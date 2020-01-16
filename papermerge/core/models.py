import subprocess
import os
import logging
import kombu

from django.conf import settings
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import (Group, Permission)
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.models import (
    PolymorphicMPTTModel,
    PolymorphicTreeForeignKey
)

from pmworker import (endpoint, storage, step)
from pmworker.pdfinfo import get_pagecount
from pmworker.storage import (
    upload_document_to_s3,
    copy2doc_url
)
from pmworker.tasks import ocr_page

from papermerge.core import mixins
from papermerge.core.storage import is_storage_left

logger = logging.getLogger(__name__)


def get_file_title(filepath):

    return os.path.basename(filepath)


def get_file_size(filepath):

    return os.path.getsize(filepath)


def get_root_user():
    user = User.objects.get(
        is_staff=True,
        is_superuser=True
    )

    return user


def get_media_root():
    return endpoint.Endpoint(f"local:{settings.MEDIA_ROOT}")


def get_storage_root():
    return endpoint.Endpoint(settings.STORAGE_ROOT)


class User(AbstractUser):
    # increases with every imported document
    # decreases with every deleted document
    # when reaches settings.USER_PROFILE_USER_STORAGE_SIZE
    # no more documents can be imported
    current_storage_size = models.BigIntegerField(default=0)

    def update_current_storage(self):
        user_docs = Document.objects.filter(user=self)
        self.current_storage_size = sum(int(doc.size) for doc in user_docs)
        self.save()


class BaseTreeNode(PolymorphicMPTTModel):
    parent = PolymorphicTreeForeignKey(
        'self',
        models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('parent')
    )
    title = models.CharField(
        _("Title"),
        max_length=200
    )

    lang = models.CharField(
        _('Language'),
        max_length=8,
        blank=False,
        null=False,
        default='deu'
    )

    user = models.ForeignKey(User, models.CASCADE)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # these columns are updated by update_index commands
    # and are used only for FTS
    ancestors_deu = SearchVectorField(null=True)
    ancestors_eng = SearchVectorField(null=True)
    title_deu = SearchVectorField(null=True)
    title_eng = SearchVectorField(null=True)

    def _get_access_diff_updated(self, new_access_list=[]):
        """
        gathers AccessDiff with updated operation
        """
        updates = AccessDiff(op=AccessDiff.UPDATE)

        for current in self.access_set.all():
            for new_access in new_access_list:
                if new_access == current and current.perm_diff(new_access):
                    updates.add(new_access)

        return updates

    def _get_access_diff_deleted(self, new_access_list=[]):
        """
        gathers AccessDiff with deleted operation
        """
        dels = AccessDiff(op=AccessDiff.DELETE)

        # if current access is not in the new list
        # it means current access was deleted.
        for current in self.access_set.all():
            if current not in new_access_list:
                dels.add(current)

        return dels

    def _get_access_diff_added(self, new_access_list=[]):
        """
        gathers AccessDiff with added operation
        """
        adds = AccessDiff(op=AccessDiff.ADDED)

        # if current access is not in the new list
        # it means current access was deleted.
        all_current = self.access_set.all()

        # if new access is not in current access list of the
        # node - it means it will be added.
        for new_access in new_access_list:
            if new_access not in all_current:
                adds.add(new_access)

        return adds

    def get_access_diffs(self, new_access_list=[]):
        """
        * access_list is a list of Access model instances.

        Returns a list of instances of AccessDiff
        between current node access list and given access list.

        Returned value will be empty list if access_list is same
        as node's current access.
        Returned value will be a list with one entry if one or
        several access were added.
        Returned value will be a list with one entry if one or
        several access were removed.
        Returned value will be a list with two entries if one or
        several access were added and one or several entries were
        removed.
        """
        ret = []
        ret.append(
            self._get_access_diff_updated(new_access_list)
        )
        ret.append(
            self._get_access_diff_added(new_access_list)
        )
        ret.append(
            self._get_access_diff_deleted(new_access_list)
        )

        return ret

    def _apply_access_diff_add(self, access_diff):
        if access_diff.is_add():
            for access in access_diff:
                Access.create(
                    node=self,
                    access_inherited=True,
                    access=access
                )

    def _apply_access_diff_delete(self, access_diff):
        if access_diff.is_delete():
            ids_to_delete = []
            for existing_access in self.access_set.all():
                for new_access in access_diff:
                    if existing_access == new_access:
                        ids_to_delete.append(
                            existing_access.id
                        )
            Access.objects.filter(id__in=ids_to_delete).delete()

    def _apply_access_diff_update(self, access_diff):
        if access_diff.is_update():
            for existing_access in self.access_set.all():
                for new_access in access_diff:
                    existing_access.update_from(new_access)

    def apply_access_diff(self, access_diff):
        self._apply_access_diff_add(access_diff)
        self._apply_access_diff_update(access_diff)
        self._apply_access_diff_delete(access_diff)

    def replace_access_diff(self, access_diff):
        # delete exiting
        self.access_set.all().delete()

        # replace with new ones
        for access in access_diff:
            Access.create(
                node=self,
                access_inherited=True,
                access=access
            )

    def apply_access_diffs(self, access_diffs):
        for x in access_diffs:
            if x.is_update() or x.is_add() or x.is_delete():
                # add (new), update (existing) or delete(existing)
                self.apply_access_diff(x)
            elif x.is_replace():
                self.replace_access_diff(x)

    def propagate_access_changes(
        self,
        access_diffs,
        apply_to_self
    ):
        """
        Adds new_access permission to self AND all children.
        """

        if (apply_to_self):
            self.apply_access_diffs(access_diffs)

        children = self.get_children()
        if children.count() > 0:
            for node in children:
                node.apply_access_diffs(access_diffs)
                node.propagate_access_changes(
                    access_diffs,
                    apply_to_self=False
                )

    class Meta(PolymorphicMPTTModel.Meta):
        # please do not confuse this "Documents" verbose name
        # with real Document object, which is derived from BaseNodeTree.
        # The reason for this naming confusing is that from the point
        # of view of users, the BaseNodeTree are just a list of documents.
        verbose_name = _("Documents")
        verbose_name_plural = _("Documents")
        _icon_name = 'basetreenode'


class AccessDiff:
    """
    A list of access permissions wich an operation
    associated.

    This structure is necessary because of the access permissions
    propagation from parent to child nodes i.e. if some access(es)
    is (are) applied to a node - it will affect (update, insert, delete)
    all its descendents.
    """
    DELETE = -1
    UPDATE = 0
    ADD = 1  # accesses in the list will be added
    REPLACE = 2

    def __init__(self, operation, access_set=[]):
        self._op = operation

        if len(access_set) == 0:
            self._set = set()
        else:
            self._set = access_set

    @property
    def operation(self):
        return self._op

    def add(self, access):
        self._set.add(access)

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter(self._set)

    def pop(self):
        return self._set.pop()

    def is_update(self):
        return self.operation == self.UPDATE

    def is_add(self):
        return self.operation == self.ADD

    def is_delete(self):
        return self.operation == self.DELETE

    def is_replace(self):
        return self.operation == self.REPLACE

    def __str__(self):
        op_name = {
            self.DELETE: "delete",
            self.UPDATE: "update",
            self.ADD: "add",
            self.REPLACE: "replace"
        }
        acc_list = [
            str(acc) for acc in self._set
        ]
        op = op_name[self._op]

        return f"AccessDiff({op}, {acc_list})"

    def __repr__(self):
        return self.__str__()


class Access(models.Model):
    # Access model guards files and folder i.e. decision
    # if a user has or hasn't permission to perform any operation
    # on give node (file/folder) is made only in respect to associated
    # access models.
    #
    # Every node (file or folder) has many access entries.
    # Every access has either one group
    # or one user associated. If a node has exactly one user
    # and one group associated - there will be two access models
    # created - one for user and one for group.

    PERM_READ = "read"
    PERM_WRITE = "write"
    PERM_DELETE = "delete"
    PERM_CHANGE_PERM = "change_perm"
    PERM_TAKE_OWNERSHIP = "take_ownership"
    ALLOW = "allow"
    DENY = "deny"
    MODEL_USER = "user"
    MODEL_GROUP = "group"
    OWNER_PERMS_MAP = {
        PERM_READ: True,
        PERM_WRITE: True,
        PERM_DELETE: True,
        PERM_CHANGE_PERM: True,
        PERM_TAKE_OWNERSHIP: True
    }

    node = models.ForeignKey(
        BaseTreeNode,
        models.CASCADE,
    )
    access_type = models.CharField(
        max_length=16,
        choices=[
            (ALLOW, _('Allow')),
            (DENY, _('Deny')),
        ],
        default='allow',
    )
    # inherited access is read only
    access_inherited = models.BooleanField(
        default=False
    )
    group = models.ForeignKey(
        Group,
        verbose_name=_('group'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('user'),
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    permissions = models.ManyToManyField(
        Permission
    )

    def create(node, access_inherited, access):
        new_access = Access.objects.create(
            user=access.user,
            access_type=access.access_type,
            node=node,
            access_inherited=access_inherited
        )
        new_access.permissions.add(
            *access.permissions.all()
        )

        return access

    def perms_codenames(self):
        return {p.codename for p in self.permissions.all()}

    def __str__(self):
        #perms = [
        #    p.codename for p in self.permissions.all()
        #]
        #perms = 'PPP'
        name = ''
        if self.user:
            name = f"User({self.user.username})"
        else:
            name = f"Group({self.group.name})"

        typ = self.access_type

        return f"Access({name}, {typ}, ...)"

    class Meta:
        permissions = [
            ("read", "Read Access"),
            ("write", "Write Access"),
            ("delete", "Delete Access"),
            ("change_perm", "Change Permissions Access"),
            ("take_ownership", "Take Ownership Access"),
        ]

    def __hash__(self):
        if self.user:
            name = f"User({self.user.username})"
        else:
            name = f"Group({self.group.name})"

        typ = self.access_type
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        return hash((name, typ))

    def __eq__(self, access):
        """
        Two access models are equal if all conditions
        are true:
        * accesses are attached to the some node
        * have same access type (allow or deny)
        * have both either same user or same group

        NOTE: inheritance flag does not matter.
        """
        if self.node.id != access.node.id:
            return False

        if self.user and access.user:
            return self.user == access.user

        if self.group and access.group:
            return self.group == access.group

        return False

    def has_perm(self, codename):
        return self.permissions.filter(
            codename=codename
        ).count() > 0

    def extract_perm_dict(self):
        result = {
            Access.PERM_READ: False,
            Access.PERM_WRITE: False,
            Access.PERM_DELETE: False,
            Access.PERM_CHANGE_PERM: False,
            Access.PERM_TAKE_OWNERSHIP: False
        }
        for perm in self.permissions.all():
            result[perm.codename] = True

        return result

    def perm_diff(self, compare_with):
        """
        passed compare with can be either:
        * a dictionary {'read': true, 'delete': false} etc
        * another Access model instance
        """
        perm_dict1 = self.extract_perm_dict()

        if isinstance(compare_with, Access):
            perm_dict2 = compare_with.extract_perm_dict()

        if isinstance(compare_with, dict):
            perm_dict2 = compare_with

        return perm_dict1 != perm_dict2

    def set_perms(self, perm_hash):

        content_type = ContentType.objects.get(
            app_label="core",
            model="access",
        )
        codenames = [
            key for key, value in perm_hash.items() if perm_hash[key]
        ]
        perms = Permission.objects.filter(
            codename__in=codenames,
            content_type=content_type
        )
        self.permissions.clear()
        if perms.count() > 0:
            self.permissions.add(*perms)

    def update_from(self, access):
        if not self.match(access):
            return False

        self.access_type = access.access_type
        self.permissions.clear()
        self.permissions.set(
            access.permissions.all()
        )


class Document(mixins.ExtractIds, BaseTreeNode):

    class CannotUpload(Exception):
        pass

    #: reference to original file, usually a pdf document with
    #: no post-processing performed on this file.
    file_orig = models.FileField(
        max_length=512,
        help_text="Reference to originaly imported file"
    )
    #: basename + ext of uploaded file.
    #: other path details are deducted from user_id and document_id
    file_name = models.CharField(
        max_length=1024,
        default=''
    )

    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )

    size = models.BigIntegerField(
        help_text="Size of file_orig attached. Size is in Bytes",
        blank=False,
        null=False,
    )

    digest = models.CharField(
        max_length=512,
        unique=True,
        help_text="Digest of file_orig attached. Size is in Bytes."
        "It is used to figure out if file was already processed.",
        blank=True,
        null=True
    )

    page_count = models.IntegerField(
        blank=False,
        default=1
    )

    text = models.TextField()

    celery_task_id = models.UUIDField(blank=True, null=True, default=None)

    # columns used only for FTS (updated by update_index)
    text_deu = SearchVectorField(null=True)
    text_eng = SearchVectorField(null=True)

    PREVIEW_HEIGHTS = (100, 300, 500)

    SMALL = PREVIEW_HEIGHTS[0]
    MEDIUM = PREVIEW_HEIGHTS[1]
    LARGE = PREVIEW_HEIGHTS[2]

    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")

    def __str__(self):
        if self.title:
            return self.title

        return "Doc {}".format(self.id)

    def reload(self):
        new_self = self.__class__.objects.get(pk=self.pk)
        self.__dict__.update(new_self.__dict__)

    @property
    def file_ext(self):
        _, ext = os.path.splitext(self.file_name)
        return ext

    def create_pages(self):
        # Q: why doc.page_count is a valid value and yet there
        #  are no pages assigned to document model ?
        # Because page count is retrieves not via models, but by invoking
        # an external utility on pdf file!
        page_count = self.page_count

        for page_index in range(1, page_count + 1):

            preview = reverse(
                'core:preview',
                args=[self.id, 800, page_index]
            )

            self.page_set.create(
                user=self.user,
                number=page_index,
                image=preview,
                lang=self.lang,
                page_count=page_count
            )

    def update_text_field(self):
        """Update text field from associated page.text fields.

        It will update text field of all associated pages first
        (from .txt files) and then concatinate all text field
        into doc.text field.

        Returns True if document contains non empty non whitespace
        text (i.e it was OCRed)
        """
        text = ""

        for page in self.page_set.all():
            if len(page.text) == 0:
                page.update_text_field()
                page.save()
                logger.debug(
                    f"text saved. len(page.text)=={len(page.text)}"
                )
            else:
                logger.info(
                    f"document_log "
                    f" username={page.user.username}"
                    f" doc_id={page.document.id}"
                    f" page_num={page.number}"
                    f" text_len={len(page.text.strip())}"
                )

            text = text + ' ' + page.text

        self.text = text.strip()
        self.save()

        return len(text.strip()) != 0

    @staticmethod
    def get_default_language():
        user = get_root_user()
        lang = user.preferences['ocr__OCR_Language']
        return lang

    @staticmethod
    def import_file(
        filepath,
        username=None,
        file_title=None,
        inbox_title="Inbox",
        delete_after_import=False,
        start_ocr_async=True,
        upload=True
    ):
        """
        Gets as input a path to a file on a local file system and:
            1. creates a document instance (if there is a available space).
            2. Copies file to doc_instance.url()
            3. (optionally) uploads the document to S3 storage.
            4. (optionally) starts ocr_async task.

        Is used on customers instance by:
            * import_file command - to import files from SFTP directory
            * import_attachment command - to import attachments from mailbox
        """
        logger.debug(f"Importing file {filepath}")

        if username is None:
            user = get_root_user()
        else:
            user = User.objects.get(username=username)

        if file_title is None:
            file_title = get_file_title(filepath)

        if not is_storage_left(
            filepath,
            user=user
        ):
            logger.error(
                f"user.username reached his disk quota"
            )
            return False

        lang = Document.get_default_language()
        # get_pagecount() might raise an exception in case
        # file is either wrong (not a PDF) or not yet
        # completed to upload
        try:
            page_count = get_pagecount(filepath)
        except Exception:
            # which means that document is not yet fully
            # uploaded by SFTP client.
            logger.error(f"File {filepath} not yet ready for importing.")
            return False

        inbox, _ = Folder.objects.get_or_create(
            title=inbox_title,
            parent=None,
            user=user
        )
        doc = Document.create_document(
            user=user,
            title=file_title,
            size=get_file_size(filepath),
            lang=lang,
            file_name=file_title,
            parent_id=inbox.id,
            page_count=page_count
        )
        logger.debug(
            f"Uploading file {filepath} to {doc.doc_ep.url()}"
        )
        # Import file is executed as root (import-file.service)
        # (because import-file need to access/delete sftp files, folder
        # as of another system user)
        # Thus, after copying file into (newly created) folders,
        # it need to change permissions (of newly created files and folders)
        # to the app_user/app_group.
        copy2doc_url(
            src_file_path=filepath,
            doc_url=doc.doc_ep.url(),
            user=settings.APP_USER,
            group=settings.APP_GROUP
        )

        if upload and settings.S3:
            upload_document_to_s3(
                doc.doc_ep
            )

        if start_ocr_async and settings.OCR:
            Document.ocr_async(
                document=doc,
                page_count=page_count,
                lang=lang,
                s3_enabled=settings.S3
            )

        if delete_after_import:
            os.remove(filepath)

        return True

    @staticmethod
    def ocr_async(
        document,
        page_count,
        lang,
        s3_enabled=False
    ):

        logger.debug("apply async begin...")
        try:
            user_id = document.user.id
            document_id = document.id
            file_name = document.file_name
            for page_num in range(1, page_count + 1):
                ocr_page.apply_async(kwargs={
                    'user_id': user_id,
                    'document_id': document_id,
                    'file_name': file_name,
                    'page_num': page_num,
                    's3_upload': s3_enabled,
                    's3_download': s3_enabled,
                    'lang': lang},
                    queue='papermerge'
                )
                document.save()
        except kombu.exceptions.OperationalError:
            logger.warning("Broker is down, skipping OCR")

        logger.debug("apply async end...")

    @staticmethod
    def create_document(
        user,
        title,
        lang,
        size,
        page_count,
        file_name,
        notes=None,
        parent_id=None,
    ):
        """
        Arguments:
            tmp_uploaded_file = an instance of
                django.core.files.uploadedfile.TemporaryUploadedFile
        """
        if parent_id is None or parent_id == '':
            parent = None
        else:
            try:
                parent = BaseTreeNode.objects.get(id=parent_id)
            except BaseTreeNode.DoesNotExist:
                parent = None
        doc = Document(
            title=title,
            size=size,
            lang=lang,
            user=user,
            parent=parent,
            notes=notes,
            file_name=file_name,
            page_count=page_count,
        )

        doc.save()
        doc.create_pages()

        return doc

    def convert_to_pdf(self):
        """
        If attached file is tiff, then convert it to PDF
        """
        if self.is_tiff:
            path_base, ext = os.path.splitext(self.file_path)
            name_base, ext = os.path.splitext(self.file_name)
            new_file_name = "{}.pdf".format(name_base)
            new_file_path = "{}.pdf".format(path_base)
            try:
                subprocess.run(
                    [
                        "/usr/bin/convert",
                        self.file_path,
                        new_file_path,
                    ],
                    check=True
                )
            except Exception as e:
                print(e.stderr)
                raise

        self.file_name = new_file_name
        self.title = new_file_name
        self.save()

    @property
    def is_tiff(self):
        base, ext = os.path.splitext(self.file_path)
        if ext and ext.lower() in (".tiff",):
            return True

        return False

    @property
    def doc_ep(self):
        result = endpoint.DocumentEp(
            user_id=self.user.id,
            document_id=self.id,
            file_name=self.file_name,
            local_endpoint=get_media_root(),
            remote_endpoint=get_storage_root()
        )

        return result

    @property
    def page_eps(self):
        """
        Enables document instance to get quickly page
        endpoints:

            page_ep = doc.page_eps[2]
            page_ep.url() # local url to second page of the doc.

        This is shortcut method when most used Step(1) is required.
        """

        results = [None]  # indexing starts from 1

        # doc.page_count might be wrong because per
        # page logic was added just recently. So, let's use
        # this opportunity and correct it!
        page_count = get_pagecount(self.doc_ep.url())

        if page_count != self.page_count:
            self.page_count = page_count
            self.save()

        for page_num in range(1, page_count + 1):
            ep = endpoint.PageEp(
                document_ep=self.doc_ep,
                page_num=page_num,
                step=step.Step(1),
                page_count=self.page_count
            )
            results.append(ep)

        return results

    def get_page_ep(self, page_num, step):
        """
        For Step(1) shortcut, use doc_instance.page_eps property.
        """
        return endpoint.PageEp(
            document_ep=self.doc_ep,
            page_num=page_num,
            step=step,
            page_count=self.page_count
        )

    @property
    def file_path(self):
        return os.path.join(
            self.dir_path,
            self.file_name
        )

    def preview_path(self, page, size=None):

        if page > self.page_count or page < 0:
            raise ValueError("Page index out of bound")

        file_name = os.path.basename(self.file_name)
        root, _ = os.path.splitext(file_name)
        page_count = self.pages_num

        if not size:
            size = "orig"

        if page_count <= 9:
            fmt_page = "{root}-page-{num:d}.{ext}"
        elif page_count > 9 and page_count < 100:
            fmt_page = "{root}-page-{num:02d}.{ext}"
        elif page_count > 100:
            fmt_page = "{root}-page-{num:003d}.{ext}"

        return os.path.join(
            self.dir_path,
            str(size),
            fmt_page.format(
                root=root, num=int(page), ext="jpg"
            )
        )

    @property
    def name(self):
        root, ext = os.path.splitext(self.file_name)
        return root

    def move_to(self, folder_id):

        folder = Folder.objects.get(id=folder_id)
        self.folder = folder
        self.pinned = True
        self.save()


class Page(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, models.CASCADE)

    number = models.IntegerField(default=1)
    page_count = models.IntegerField(default=1)

    text = models.TextField(default='')

    lang = models.CharField(
        max_length=8,
        blank=False,
        null=False,
        default='deu'
    )
    text_deu = SearchVectorField(null=True)
    text_eng = SearchVectorField(null=True)

    @property
    def page_ep(self):
        return endpoint.PageEp(
            document_ep=self.document.doc_ep,
            page_num=self.number,
            page_count=self.page_count
        )

    def update_text_field(self):
        """Update text field from associated .txt file.

        Returns non-empty text string value if .txt file was found.
        If file was not found - will return an empty string.
        """
        if not settings.OCR:
            return ''

        text = ''
        logger.debug(f"Checking {self.txt_url}")

        if not self.txt_exists:
            logger.debug(
                f"Missing page txt {self.txt_url}."
            )
            if not storage.download(self.page_ep):
                logger.info(
                    f"document_log "
                    f" username={self.user.username}"
                    f" doc_id={self.document.id}"
                    f" page_num={self.number}"
                    f" text_len={len(text.strip())}"
                )
                return ''
        else:
            logger.debug(f"Page txt {self.txt_url} exists.")

        with open(self.txt_url) as file_handle:
            self.text = file_handle.read()
            self.save()
            logger.debug(
                f"text saved. len(page.text)=={len(self.text)}"
            )
            text = self.text
            logger.info(
                f"document_log "
                f" username={self.user.username}"
                f" doc_id={self.document.id}"
                f" page_num={self.number}"
                f" text_len={len(self.text.strip())}"
            )

        return text

    def image_preview_missing():
        from django.contrib.staticfiles.templatetags.staticfiles import static

        return static("supervisor/img/missing_page.png")

    image = models.CharField(
        max_length=1024,
        default=image_preview_missing
    )

    @property
    def txt_url(self):

        result = endpoint.PageEp(
            document_ep=self.document.doc_ep,
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_url()

    @property
    def txt_exists(self):

        result = endpoint.PageEp(
            document_ep=self.document.doc_ep,
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_exists()


class Folder(mixins.ExtractIds, BaseTreeNode):

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.title
