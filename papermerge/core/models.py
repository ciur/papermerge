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

from mglib.path import (DocumentPath, PagePath)
from pmworker.pdfinfo import get_pagecount
from pmworker.storage import (
    upload_document_to_s3,
    copy2doc_url
)
from pmworker import pdftk
from pmworker import ocrmigrate
from pmworker.tasks import ocr_page

from papermerge.core import mixins

logger = logging.getLogger(__name__)


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

    # Obsolete columns. Replaced by ancestors_fts
    ancestors_deu = SearchVectorField(null=True)
    ancestors_eng = SearchVectorField(null=True)
    # Obsolete columns. Replaced by title_fts
    title_deu = SearchVectorField(null=True)
    title_eng = SearchVectorField(null=True)

    # this column is updated by update_fts command
    ancestors_fts = SearchVectorField(null=True)
    title_fts = SearchVectorField(null=True)

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

    # Document's version start with 0 (0 = default value)
    # Document's version is incremented everytime pdftk operation
    # is applied to it (page delete, page rotate, page reorder).
    # Versioning is on file level. Means - there is no such thing as model
    # level versioning. I think this will complicate everthing just too much.
    # At any point in time, user sees/works with/searches only last version.
    version = models.IntegerField(
        blank=True,
        null=True,
        default=0
    )
    # Q: If there is no model versions, why version is introduced at all?
    # A: pdftk on every operation creates a new file... well, that new
    # file is the next version of the document.

    text = models.TextField()

    # Obsolete column, replaced by text_fts column.
    text_deu = SearchVectorField(null=True)
    text_eng = SearchVectorField(null=True)

    text_fts = SearchVectorField(null=True)

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

    def reorder_pages(self, new_order):
        """
        new_order is a list of following format:

            [
                {'page_num': 2, page_order: 1},
                {'page_num': 1, page_order: 2},
                {'page_num': 3, page_order: 3},
                {'page_num': 4, page_order: 4},
            ]
        Example above means that in current document of 4 pages,
        first page was swapped with second one.
        page_num    = older page order
        page_order  = current page order
        So in human language, each hash is read:
            <page_num> now should be <page_order>
        """
        if not isinstance(new_order, list):
            logger.error("Expecting list argument")
            return

        src_ep = self.doc_ep
        # reorder pages
        new_version = pdftk.reorder_pages(
            self.doc_ep,
            new_order
        )

        self.version = new_version
        self.save()
        self.recreate_pages()
        # Move OCR related text to newer versio
        # so that we can skip OCRing of the document
        migr = ocrmigrate.OcrMigrate(
            src_ep=src_ep,
            dst_ep=self.doc_ep  # endpoint with inc version
        )
        migr.migrate_reorder(
            new_order=new_order
        )

    def delete_pages(self, page_numbers):
        """
        Deletes pages with given order numbers from
        the documents:

        * locally - syncronious
        * remotely - async.
        """
        if not isinstance(page_numbers, list):
            logger.error("Expecting list argument")
            return

        src_ep = self.doc_ep
        # delete pages
        new_version = pdftk.delete_pages(
            self.doc_ep,
            page_numbers
        )

        if new_version == self.version:
            raise Exception("Expecting version to be incremented")

        self.version = new_version
        self.save()
        # update pages model
        self.recreate_pages()

        # Move OCR related text files to newer version
        # (.txt + .hocr files)
        migr = ocrmigrate.OcrMigrate(
            src_ep=src_ep,
            dst_ep=self.doc_ep  # endpoint with already incremented version
        )
        migr.migrate_delete(
            deleted_pages=page_numbers
        )

    def recreate_pages(self):
        """
        Recreate page models
        """
        self.page_set.all().delete()
        self.page_count = get_pagecount(
            self.doc_ep.url()
        )
        self.save()
        self.create_pages()

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

    def paste(
        self,
        doc_pages,
        after=False,
        before=False
    ):
        """
        Paste pages in current document.
        """
        new_page_count = sum(
            [
                len(pages) for pages in doc_pages.values()
            ]
        )

        if new_page_count == 0:
            logger.warning("No pages to paste. Exiting.")
            return

        # for each document where are pages to paste
        doc_list = []
        doc_ep_list = []
        old_version = self.version

        for doc_id in doc_pages.keys():
            try:
                doc = Document.objects.get(id=doc_id)
            except Document.DoesNotExist:
                logger.warning(
                    f"While pasting, doc_id={doc_id} was not found"
                )
                return
            doc_list.append({'doc': doc, 'page_nums': doc_pages[doc_id]})
            doc_ep_list.append(
                {'doc_ep': doc.doc_ep, 'page_nums': doc_pages[doc_id]}
            )

        # returns new document version
        new_version = pdftk.paste_pages(
            dest_doc_ep=self.doc_ep,
            src_doc_ep_list=doc_ep_list,
            dest_doc_is_new=False,
            after_page_number=after,
            before_page_number=before
        )

        if new_version == self.version:
            raise Exception("Expecting version to be incremented")

        self.version = new_version
        self.save()

        # migrate document's own pages from previous
        # version (this differs from pasting into newly
        # created docs)
        doc_ep_list.insert(
            0,
            {
                'doc_ep': DocumentPath(
                    user_id=self.user.id,
                    document_id=self.id,
                    version=old_version,
                    file_name=self.file_name
                ),
                'page_nums': list(range(1, self.page_count + 1))
            }
        )

        ocrmigrate.migrate_cutted_pages(
            dest_ep=self.doc_ep,
            src_doc_ep_list=doc_ep_list
        )

        # delete pages of source document (which where
        # cutted and pasted into new doc)
        for item in doc_list:
            item['doc'].delete_pages(
                page_numbers=item['page_nums']
            )

        # must be at the end
        self.recreate_pages()

    @staticmethod
    def paste_pages(
        user,
        parent_id,
        doc_pages
    ):
        # parent_node is an instance of BaseTreeNode
        # doc_pages is a dictionary of format:
        # {
        #    doc_id_1: [page_num_1a, page_num_2a, ...],
        #    doc_id_2: [page_num_1b, page_num_2b, ...],
        #    doc_id_3: [page_num_1c, page_num_2c, ...]
        # }
        # 1. Create a new document NEWDOC
        # 2. Build new pages for the newly created document
        # num_pages = len(doc_pages[doc_id_1]) + len(doc_pages[doc_id_2]) + ...
        # 3. for each document with ids in doc_pages.keys() (DOC):
        #     a. copy pages data from DOC to NEWDOC
        #     b. deletes pages from DOC (pages mentioned in doc_page[key] list)

        new_page_count = sum(
            [
                len(pages) for pages in doc_pages.values()
            ]
        )

        if new_page_count == 0:
            logger.warning("No pages to paste. Exiting.")
            return

        # 1. Create new document
        # 2. Build new pages for newly created document
        document = Document.create_document(
            user=user,
            parent_id=parent_id,
            lang=user.preferences['ocr__OCR_Language'],
            title="pasted.pdf",
            size=0,  # will be updated later, after pdftk will create new doc
            file_name="pasted.pdf",
            page_count=new_page_count
        )

        # for each document where are pages to paste
        doc_list = []
        doc_ep_list = []
        for doc_id in doc_pages.keys():
            try:
                doc = Document.objects.get(id=doc_id)
            except Document.DoesNotExist:
                logger.warning(
                    f"While pasting, doc_id={doc_id} was not found"
                )
                return
            doc_list.append({'doc': doc, 'page_nums': doc_pages[doc_id]})
            doc_ep_list.append(
                {'doc_ep': doc.doc_ep, 'page_nums': doc_pages[doc_id]}
            )

        # returns new document version
        new_version = pdftk.paste_pages(
            dest_doc_ep=document.doc_ep,
            src_doc_ep_list=doc_ep_list,
            dest_doc_is_new=True,
            after_page_number=-1,
            before_page_number=-1
        )

        if new_version == document.version:
            raise Exception("Expecting version to be incremented")

        document.version = new_version
        document.save()
        # update pages model
        document.recreate_pages()

        ocrmigrate.migrate_cutted_pages(
            dest_ep=document.doc_ep,
            src_doc_ep_list=doc_ep_list
        )

        # delete pages of source document (which where
        # cutted and pasted into new doc)
        for item in doc_list:
            item['doc'].delete_pages(
                page_numbers=item['page_nums']
            )

        # TODO: update size of the new document (changed doc)

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
        # https://github.com/django-mptt/django-mptt/issues/568
        doc._tree_manager.rebuild()

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
    def path(self):
        version = self.version
        if not isinstance(version, int):
            version = 0

        result = DocumentPath(
            user_id=self.user.id,
            document_id=self.id,
            version=version,
            file_name=self.file_name,
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
    # Obsolete columns. Replaced by text_fts.
    text_deu = SearchVectorField(null=True)
    text_eng = SearchVectorField(null=True)

    # Replaced text_deu and text_eng
    text_fts = SearchVectorField(null=True)

    @property
    def is_last(self):
        return self.number == self.page_count

    @property
    def is_first(self):
        return self.number == 1

    @property
    def path(self):
        return PagePath(
            document_ep=self.document.doc_ep,
            page_num=self.number,
            page_count=self.page_count
        )

    def update_text_field(self):
        """Update text field from associated .txt file.

        Returns non-empty text string value if .txt file was found.
        If file was not found - will return an empty string.
        """
        text = ''
        logger.debug(f"Checking {self.txt_url}")

        if not self.txt_exists:
            logger.debug(
                f"Missing page txt {self.txt_url}."
            )
            return
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

    image = models.CharField(
        max_length=1024,
        default=''
    )

    @property
    def txt_url(self):

        result = PagePath(
            document_ep=self.document.path,
            page_num=self.number,
            page_count=self.page_count
        )

        return result.txt_url()

    @property
    def txt_exists(self):

        result = PagePath(
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


class LanguageMap(models.Model):
    """
    Data table which maps Tesseract language code (tsr_code)
    (as specified from command line argument -l <lang>) to
    postgresql language catalog (pg_catalog column).
    Examples:
        tst_code       pg_catalog          pg_short
          deu       pg_catalog.german        german
          eng       pg_catalog.english       english
          spa       pg_catalog.spanish       spanish
          rus       pg_catalog.russian       russian
          ron       pg_catalog.romanian      romanian

    Tesseract uses ISO 639-2/T or ISO 639-2/B name for language codes.
    Here is full list:
        https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

    Postgres text search configurations are listed with

        psql> \dF  # noqa

    See papermerge.code.lib.lang.LANG_DICT
    """
    tsr_code = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        unique=True
    )
    pg_catalog = models.CharField(
        max_length=64,
        blank=False,
        null=False
    )
    pg_short = models.CharField(
        max_length=64,
        blank=False,
        null=False
    )
