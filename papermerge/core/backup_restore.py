import datetime
import logging
import time
import io
import os
import tarfile
import json
from pathlib import PurePath, Path

from django.core.files.temp import NamedTemporaryFile
from pmworker.pdfinfo import get_pagecount

from papermerge.core.models import Document, User, Folder
from papermerge.core.storage import default_storage
from papermerge.core.tasks import ocr_page

logger = logging.getLogger()

_supported_versions = ["1.3.0"]


def backup_documents(backup_file: io.BytesIO):
    documents = Document.objects.all()
    current_backup = dict()
    current_backup['created'] = datetime.datetime.now()
    current_backup['version'] = "1.3.0"
    current_backup['documents'] = list()

    with tarfile.open(fileobj=backup_file, mode="w") as backup_archive:
        for current_document_object in documents:  # type: Document
            current_document = dict()
            targetPath = _createTargetPath(current_document_object)
            backup_archive.add(current_document_object.absfilepath, arcname=targetPath)
            current_document['path'] = targetPath
            current_document['lang'] = current_document_object.lang
            current_backup['documents'].append(current_document)

        json_bytes = json.dumps(current_backup, indent=4, default=str).encode('utf-8')
        tarinfo = tarfile.TarInfo(name='backup.json')
        tarinfo.size = len(json_bytes)
        tarinfo.mtime = time.time()
        backup_archive.addfile(tarinfo, io.BytesIO(json_bytes))


def restore_documents(restore_file: io.BytesIO, username):
    restore_file.seek(0)
    user = User.objects.filter(username=username).first()
    with tarfile.open(fileobj=restore_file, mode="r") as restore_archive:
        backup_json = restore_archive.extractfile('backup.json')
        backup_info = json.load(backup_json)
        for restore_file in restore_archive.getnames():
            if restore_file == "backup.json":
                continue
            for info in backup_info['documents']:
                document_info = info
                if info['path'] == restore_file:
                    break
            splitted_path = PurePath(restore_file).parts
            parent = None
            # we first have to create a folder structure
            if len(splitted_path) > 1:
                for folder in splitted_path[:-1]:
                    folder_object = Folder.objects.filter(title=folder).filter(parent=parent).first()
                    if folder_object is None:
                        new_folder = Folder.objects.create(title=folder, parent=parent, user=user)
                        parent = new_folder
                    else:
                        parent = folder_object
            document_object = Document.objects.filter(title=splitted_path[-1]).filter(parent=parent).first()
            if document_object is not None:
                logger.error("Document %s already exists, skipping", restore_file)
            else:
                with NamedTemporaryFile("w+b") as temp_output:
                    temp_output.write(restore_archive.extractfile(restore_file).read())
                    temp_output.seek(0)
                    size = os.path.getsize(temp_output.name)
                    page_count = get_pagecount(temp_output.name)
                    new_doc = Document.create_document(user=user,
                                             title=splitted_path[-1],
                                             size=size,
                                             lang=document_info['lang'],
                                             file_name=splitted_path[-1],
                                             parent_id=parent.id,
                                             notes="",
                                             page_count=page_count)
                    default_storage.copy_doc(
                        src=temp_output.name,
                        dst=new_doc.path.url()
                    )

                for page_num in range(1, page_count + 1):
                    ocr_page.apply_async(kwargs={
                        'user_id': user.id,
                        'document_id': new_doc.id,
                        'file_name': splitted_path[-1],
                        'page_num': page_num,
                        'lang': document_info['lang']}
                    )


def _can_restore(restore_file: io.BytesIO):
    with tarfile.open(fileobj=restore_file, mode="r") as restore_archive:
        backup_json = restore_archive.extractfile('backup.json')
        if backup_json is None:
            return False
        current_backup = json.load(backup_json)
        if current_backup.get('version') is not None and current_backup.get('version') in _supported_versions:
            return True


def _is_valid_user(username: str):
    current_user = User.objects.filter(username=username).first()
    if current_user is not None:
        return True
    else:
        return False


def _createTargetPath(document: Document):
    """
    Takes a document and traverses the tree to the root noting the path
    :param document: the document you want the path of
    :return: the full path from root to the document including filename
    :rtype str
    """
    targetPath = document.file_name
    currentNode = document
    while currentNode.parent is not None:
        currentNode = currentNode.parent
        targetPath = os.path.join(currentNode.title, targetPath)

    return targetPath
