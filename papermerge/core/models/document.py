import logging
import os

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from mglib import step
from mglib.path import DocumentPath, PagePath
from mglib.pdfinfo import get_pagecount
from mglib.utils import get_assigns_after_delete

from papermerge.core.storage import default_storage
from .kvstore import KVCompNode, KVNode
from .node import BaseTreeNode
from .access import Access


from papermerge.search import index

logger = logging.getLogger(__name__)


class Document(BaseTreeNode):

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
        max_length=70,
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

    PREVIEW_HEIGHTS = (100, 300, 500)

    SMALL = PREVIEW_HEIGHTS[0]
    MEDIUM = PREVIEW_HEIGHTS[1]
    LARGE = PREVIEW_HEIGHTS[2]

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

    def to_dict(self):
        item = {}

        pages = []
        for page in self.pages.all():
            pages.append(page.to_dict())

        item['id'] = self.id
        item['title'] = self.title
        item['notes'] = self.notes
        item['created_at'] = self.created_at.strftime("%d.%m.%Y %H:%M:%S")
        item['timestamp'] = self.created_at.timestamp()

        if self.parent:
            item['parent_id'] = self.parent.id
        else:
            item['parent_id'] = ''

        item['ctype'] = 'document'
        item['pages'] = pages

        tags = []
        for tag in self.tags.all():
            tags.append(tag.to_dict())
        item['tags'] = tags

        return item

    def assign_kv_values(self, kv_dict):
        """
        Assignes kv_dict of key value to its metadata
        and metadata of its pages.
        """
        logger.debug(
            f"assign_key_values kv_dict={kv_dict} doc_id={self.id}"
        )
        for key, value in kv_dict.items():
            # for self
            logger.debug(
                f"Assign to DOC key={key} value={value}"
            )
            self.kv[key] = value
            # and for all pages of the document
            for page in self.pages.all():
                logger.debug(
                    f"Assign to page number={page.number}"
                    f" key={key} value={value}"
                )
                try:
                    # Never (automatically) overwrite am
                    # existing Metadata value
                    if not page.kv[key]:
                        # page metadata value is empty fill it in.
                        page.kv[key] = value
                except Exception as e:
                    logging.error(
                        f"Error: page {page.number}, doc_id={self.id} has no key={key}", # noqa
                        exc_info=e
                    )

    @property
    def kv(self):
        return KVNode(instance=self)

    def propagate_changes(
        self,
        diffs_set,
        apply_to_self,
        attr_updates=[]
    ):
        super().propagate_changes(
            diffs_set=diffs_set,
            apply_to_self=apply_to_self,
            attr_updates=attr_updates
        )
        # Access permissions are not applicable
        # for Page models, so if diffs_set contains
        # instances of Access - just return
        if (len(diffs_set)):
            first_diff = diffs_set[0]
            if len(first_diff):
                model = list(first_diff)[0]
                if isinstance(model, Access):
                    return

        # documents need to propage changes
        # to their pages

        for page in self.pages.all():
            page.propagate_changes(
                diffs_set=diffs_set,
                apply_to_self=apply_to_self,
                attr_updates=attr_updates
            )

    @property
    def kvcomp(self):
        return KVCompNode(instance=self)

    def inherit_kv_from(self, node):
        inherited_kv = [
            {
                'key': item.key,
                'kv_type': item.kv_type,
                'kv_format': item.kv_format,
                'value': item.value,
                'kv_inherited': True
            } for item in node.kv.all()
        ]
        self.kv.update(inherited_kv)

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

        if not isinstance(new_order, list):
            logger.error("Expecting list argument")
            return

        new_version = default_storage.reorder_pages(
            doc_path=self.path,
            new_order=new_order
        )
        self.version = new_version
        self.save()
        self.recreate_pages()

    def delete_pages(
        self,
        page_numbers: list,
        skip_migration=False
    ):
        """
        Deletes pages with given order numbers from
        the documents.
        """
        if not isinstance(page_numbers, list):
            logger.error("Expecting list argument")
            return

        # delete pages
        new_version = default_storage.delete_pages(
            doc_path=self.path,
            page_numbers=page_numbers,
            skip_migration=skip_migration
        )

        if new_version == self.version:
            raise Exception("Expecting version to be incremented")

        self.version = new_version

        # total pages before delete
        total_page_count = self.pages.count()
        self.pages.filter(number__in=page_numbers).delete()
        # update self.page_count attribute
        self.page_count = self.pages.count()
        self.save()

        self.reassign_page_nums_after_delete(
            page_count=total_page_count,
            deleted_pages=page_numbers
        )

    def reassign_page_nums_after_delete(
        self,
        deleted_pages: list,
        page_count: int
    ):
        """
        :page_count: page count BEFORE delete operation
        """
        pairs = get_assigns_after_delete(
            total_pages=page_count,
            deleted_pages=deleted_pages
        )
        for new_version_page_num, old_version_page_num in pairs:
            page = self.pages.get(number=old_version_page_num)
            page.number = new_version_page_num
            page.save()

    def recreate_pages(self):
        """
        Recreate page models.
        """

        self.pages.all().delete()
        self.page_count = get_pagecount(
            default_storage.abspath(self.path.url())
        )
        self.save()
        self.create_pages()

    def create_pages(self):
        # Q: why doc.page_count is a valid value and yet there
        #  are no pages assigned to document model ?
        # Because page count is retrieved not via models, but by invoking
        # an external utility on pdf file!
        page_count = self.page_count

        for page_index in range(1, page_count + 1):

            preview = reverse(
                'core:preview',
                args=[self.id, 800, page_index]
            )

            page = self.pages.create(
                user=self.user,
                number=page_index,
                image=preview,
                lang=self.lang,
                page_count=page_count
            )
            page.inherit_kv_from(self)

    def update_text_field(self):
        """Update text field from associated page.text fields.

        It will update text field of all associated pages first
        (from .txt files) and then concatinate all text field
        into doc.text field.

        Returns True if document contains non empty non whitespace
        text (i.e it was OCRed)
        """
        text = ""
        txt_exists = False

        for page in self.pages.all():
            if len(page.text) == 0:
                txt_exists = page.update_text_field()
                # in case .txt for one page is not present - interrupt
                # the whole iteration
                if txt_exists:
                    page.save()
                    logger.debug(
                        f"text saved. len(page.text)=={len(page.text)}"
                    )
                else:
                    # interrupt - if one page's .txt was not found.
                    break
            else:
                logger.debug(
                    f"document_log "
                    f" username={page.user.username}"
                    f" doc_id={page.document.id}"
                    f" page_num={page.number}"
                    f" text_len={len(page.text.strip())}"
                )

            text = text + ' ' + page.text

        if txt_exists:
            # Save this document only in case all .txt
            # were present, otherwise running ./manage.py worker
            # will 'resurrect' deleted documents.
            self.text = text.strip()
            self.save()

        return len(text.strip()) != 0

    @staticmethod
    def paste_pages(
        user,
        parent_id,
        doc_pages,
        dst_document=None,
        after=False,
        before=False,
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
        dst_doc_is_new = False
        if not dst_document:
            dst_document = Document.create_document(
                user=user,
                parent_id=parent_id,
                lang=user.preferences['ocr__OCR_Language'],
                title="pasted.pdf",
                size=0,  # updated later, after pdftk will create new doc
                file_name="pasted.pdf",
                page_count=new_page_count
            )
            dst_doc_is_new = True

        # for each document where are pages to paste
        doc_list = []
        data_list = []
        for doc_id in doc_pages.keys():
            try:
                doc = Document.objects.get(id=doc_id)
            except Document.DoesNotExist:
                logger.warning(
                    f"While pasting, doc_id={doc_id} was not found"
                )
                return

            src = default_storage.abspath(doc.path)
            doc_path = doc.path

            doc_list.append({'doc': doc, 'page_nums': doc_pages[doc_id]})
            data_list.append(
                {
                    'src': src,
                    'doc_path': doc_path,
                    'page_nums': doc_pages[doc_id]
                }
            )

        # returns new document version
        new_version = default_storage.paste_pages(
            dest_doc_path=dst_document.path,
            data_list=data_list,
            dest_doc_is_new=dst_doc_is_new,
            after_page_number=after,
            before_page_number=before
        )

        if new_version == dst_document.version:
            raise Exception("Expecting version to be incremented")

        dst_document.version = new_version
        dst_document.save()
        # update pages model
        dst_document.recreate_pages()

        # delete pages of source document (which where
        # cutted and pasted into new doc)
        for item in doc_list:
            item['doc'].delete_pages(
                page_numbers=item['page_nums']
            )

        return dst_document
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
        digest=None,
        rebuild_tree=True  # obsolete
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
            digest=digest
        )
        
        doc.validate_unique()
        doc.save()
        # Important! - first document must inherit metakeys from
        # parent folder
        if parent:
            doc.inherit_kv_from(parent)

        # and only afterwards create pages must be called.
        # create_pages will trigger metadata keys from document
        # to the created pages.
        doc.create_pages()

        return doc

    @property
    def absfilepath(self):
        return default_storage.abspath(
            self.path.url()
        )

    def vpath(self, version=0):
        result = DocumentPath(
            user_id=self.user.id,
            document_id=self.id,
            version=version,
            file_name=self.file_name,
        )

        return result

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
    def page_paths(self):
        """
        Enables document instance to get quickly page
        paths:

            page_path = doc.page_path[2]
            page_path.url() # local url to second page of the doc.

        This is shortcut method when most used Step(1) is required.
        """

        results = [None]  # indexing starts from 1

        # doc.page_count might be wrong because per
        # page logic was added just recently. So, let's use
        # this opportunity and correct it!
        page_count = get_pagecount(self.absfilepath)

        if page_count != self.page_count:
            self.page_count = page_count
            self.save()

        for page_num in range(1, page_count + 1):
            page_path = PagePath(
                document_path=self.path,
                page_num=page_num,
                step=step.Step(1),
                page_count=self.page_count
            )
            results.append(page_path)

        return results

    def get_page_path(self, page_num, step):
        """
        For Step(1) shortcut, use doc_instance.page_eps property.
        """
        return PagePath(
            document_path=self.path,
            page_num=page_num,
            step=step,
            page_count=self.page_count
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

    def add_tags(self, tags):
        """
        tags is an iteratable of papermerge.core.models.Tag instances
        """
        for tag in tags:
            self.tags.add(
                tag,
                tag_kwargs={'user': self.user}
            )
    def validate_unique(self, exclude=None):
        """
        check if user already uploaded this file
        """
        same_documents = Document.objects.filter(digest=self.digest)
        if same_documents.filter(user=self.user).exists():
            raise ValidationError("{} already has this document".format(self.user))
