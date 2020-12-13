import datetime
import logging
import time
import io
import os
import tarfile
import json
from pathlib import PurePath

from django.core.files.temp import NamedTemporaryFile
from mglib.pdfinfo import get_pagecount

from papermerge.core import __version__ as PAPERMERGE_VERSION
from papermerge.core.models import (
    Document,
    User,
    Folder,
    Tag,
    BaseTreeNode
)
from papermerge.core.storage import default_storage
from papermerge.core.utils import remove_backup_filename_id
from papermerge.core.tasks import ocr_page

logger = logging.getLogger(__name__)


def backup_documents(
    backup_file: io.BytesIO,
    user: User,
    include_user_password=False
):
    """
    Backup all documents for specific user.

    :include_user_password: if set to True,  will add to backup archive digest
        of user password.
    """

    current_backup = dict()
    current_backup['created'] = datetime.datetime.now()
    current_backup['version'] = PAPERMERGE_VERSION

    with tarfile.open(fileobj=backup_file, mode="w") as backup_archive:

        if user:
            current_backup['documents'] = list()
            _add_user_documents(
                user,
                current_backup,
                backup_archive,
                include_user_in_path=False
            )
        else:
            current_backup['users'] = list()
            for user in User.objects.all():
                current_user = {
                    'username': user.username,
                    'email': user.email,
                    'is_superuser': user.is_superuser,
                    'is_active': user.is_active,
                    'documents': []
                }
                if include_user_password:
                    # raw digest of user's password
                    current_user['password'] = user.password
                _add_user_documents(
                    user,
                    current_user,
                    backup_archive,
                    include_user_in_path=True
                )
                current_backup['users'].append(current_user)

        json_bytes = json.dumps(
            current_backup,
            indent=4,
            default=str
        ).encode('utf-8')

        tarinfo = tarfile.TarInfo(name='backup.json')
        tarinfo.size = len(json_bytes)
        tarinfo.mtime = time.time()

        backup_archive.addfile(tarinfo, io.BytesIO(json_bytes))


def restore_documents(
    restore_file: io.BytesIO,
    user: User,
    skip_ocr=False
):

    restore_file.seek(0)

    with tarfile.open(fileobj=restore_file, mode="r") as restore_archive:
        backup_json = restore_archive.extractfile('backup.json')
        backup_info = json.load(backup_json)

        leading_user_in_path = False
        _user = user
        if not user:
            leading_user_in_path = True
            # user was not specified. It is assument that
            # backup.json contains a list of users.
            # Thus recreate users first.
            for backup_user in backup_info['users']:
                user = User.objects.create(
                    username=backup_user['username'],
                    email=backup_user['email'],
                    is_active=backup_user['is_active'],
                    is_superuser=backup_user['is_superuser']
                )
                # in case --include-user-password switch was used
                # update user (raw digest of) password field
                password = backup_user.get('password')
                if password:
                    user.password = password
                    user.save()

        for restore_file in restore_archive.getnames():

            if restore_file == "backup.json":
                continue

            logger.debug(f"Restoring file {restore_file}...")

            splitted_path = PurePath(restore_file).parts
            base, ext = os.path.splitext(
                remove_backup_filename_id(splitted_path[-1])
            )

            # if there is leading username, remove it.
            if leading_user_in_path:
                username = splitted_path[0]
                _user = User.objects.get(username=username)
                splitted_path = splitted_path[1:]

            if backup_info.get('documents', False):
                backup_info_documents = backup_info['documents']
            else:
                backup_info_documents = _get_json_user_documents_list(
                    backup_info,
                    _user
                )
                leading_user_in_path = True

            for info in backup_info_documents:
                document_info = info
                if info['path'] == restore_file:
                    break

            parent = None

            # variables used only to shorten debug message
            _sp = splitted_path
            _rf = restore_file
            logger.debug(
                f"{_rf}: splitted_path={_sp} len(splitted_path)={len(_sp)}"
            )
            # we first have to create a folder structure
            if len(splitted_path) > 1:
                for folder in splitted_path[:-1]:

                    folder_object = Folder.objects.filter(
                        title=folder,
                        user=_user
                    ).filter(parent=parent).first()

                    if folder_object is None:
                        new_folder = Folder.objects.create(
                            title=folder,
                            parent=parent,
                            user=_user
                        )
                        parent = new_folder
                    else:
                        parent = folder_object

            with NamedTemporaryFile("w+b", suffix=ext) as temp_output:
                logger.debug(f"Extracting {restore_file}...")

                ff = restore_archive.extractfile(restore_file)
                temp_output.write(
                    ff.read()
                )
                temp_output.seek(0)
                size = os.path.getsize(temp_output.name)

                page_count = get_pagecount(temp_output.name)

                if parent:
                    parent_id = parent.id
                else:
                    parent_id = None

                new_doc = Document.objects.create_document(
                    user=_user,
                    title=document_info['title'],
                    size=size,
                    lang=document_info['lang'],
                    file_name=remove_backup_filename_id(splitted_path[-1]),
                    parent_id=parent_id,
                    notes="",
                    page_count=page_count,
                    rebuild_tree=False  # speeds up 100x
                )

                tag_attributes = document_info.get('tags', [])

                for attrs in tag_attributes:
                    attrs['user'] = _user
                    tag, created = Tag.objects.get_or_create(**attrs)
                    new_doc.tags.add(tag)

                default_storage.copy_doc(
                    src=temp_output.name,
                    dst=new_doc.path().url()
                )

            if not skip_ocr:
                for page_num in range(1, page_count + 1):
                    ocr_page.apply_async(kwargs={
                        'user_id': _user.id,
                        'document_id': new_doc.id,
                        'file_name': new_doc.file_name,
                        'page_num': page_num,
                        'lang': document_info['lang']}
                    )


def build_tar_archive(
    fileobj: io.BytesIO,
    node_ids: list
):
    """
    Builds a tar archive with given node ids documents.

    This function is used to download selected documents and folders.
    :fileobj: is a file which will be sent to the client side as
        content disposition.
    """
    with tarfile.open(fileobj=fileobj, mode="w") as archive:
        _rec_tar_archive(
            archive=archive,
            node_ids=node_ids,
            # at the beginning the list of parent names is
            # emtpy
            abspath=[]
        )


def _rec_tar_archive(
    archive,
    node_ids,
    abspath
):
    """
    Recursively builds a tar archive based on folder structure of
    BaseTreeNode instances.

    :node_ids: a list of node ids (node = instance of BaseTreeNode)
    :abspath: a list of folder parent names
    """

    for node in BaseTreeNode.objects.filter(id__in=node_ids):

        if node.is_document():

            arc_path = os.path.join(
                # add document to the current_depth
                *abspath,
                node.title
            )
            archive.add(
                node.absfilepath,
                arcname=arc_path
            )
        elif node.is_folder():

            child_ids = [
                child.id for child in node.get_children()
            ]
            _rec_tar_archive(
                archive,
                child_ids,
                abspath + [node.title]
            )


def _can_restore(restore_file: io.BytesIO):
    with tarfile.open(fileobj=restore_file, mode="r") as restore_archive:
        backup_json = restore_archive.extractfile('backup.json')
        if backup_json is None:
            return False
        current_backup = json.load(backup_json)

        if current_backup.get('version') is not None:
            return True


def _is_valid_user(username: str):
    current_user = User.objects.filter(username=username).first()
    if current_user is not None:
        return True
    else:
        return False


def _createTargetPath(document: Document, include_user_in_path=False):
    """
    Takes a document and traverses the tree to the root noting the path
    :param document: the document you want the path of
    :return: the full path from root to the document including filename
    :rtype str
    """
    # make filename unique
    targetPath = f"{document.file_name}__{document.id}"
    currentNode = document
    while currentNode.parent is not None:
        currentNode = currentNode.parent
        targetPath = os.path.join(
            currentNode.title,
            targetPath
        )

    if include_user_in_path:
        targetPath = os.path.join(
            document.user.username, targetPath
        )

    return targetPath


def _add_current_document_entry(
    document,
    include_user_in_path=False
):
    current_document = {}

    targetPath = _createTargetPath(
        document,
        include_user_in_path=include_user_in_path
    )
    tags = [tag.to_dict() for tag in document.tags.all()]

    current_document['path'] = targetPath
    current_document['lang'] = document.lang
    current_document['title'] = document.title
    current_document['tags'] = tags

    return current_document


def _get_json_user_documents_list(json_backup: dict, user: User):
    for _u in json_backup['users']:
        if _u['username'] == user.username:
            return _u['documents']

    return None


def _add_user_documents(
    user,
    current_backup,
    backup_archive,
    include_user_in_path=False
):
    documents = Document.objects.filter(user=user)

    for current_document_object in documents:  # type: Document
        try:
            backup_archive.add(
                current_document_object.absfilepath,
                arcname=_createTargetPath(
                    current_document_object,
                    include_user_in_path=include_user_in_path
                )
            )
            current_document = _add_current_document_entry(
                current_document_object,
                include_user_in_path=include_user_in_path
            )
            current_backup['documents'].append(
                current_document
            )
        except Exception as e:
            # Log error, but continue backup process
            logger.exception(
                f"Error {e} occurred."
            )
