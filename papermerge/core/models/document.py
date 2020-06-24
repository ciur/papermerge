import logging
import os

from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mglib import step
from mglib.path import DocumentPath, PagePath
from mglib.pdfinfo import get_pagecount
from papermerge.core import mixins
from papermerge.core.models.kvstore import KVCompNode, KVNode
from papermerge.core.models.node import BaseTreeNode
from papermerge.core.storage import default_storage
from papermerge.search import index

logger = logging.getLogger(__name__)


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

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

    @property
    def kv(self):
        return KVNode(instance=self)

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
        page_numbers,
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
        self.save()
        # update pages model
        self.recreate_pages()

    def recreate_pages(self):
        """
        Recreate page models
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
        # Because page count is retrieves not via models, but by invoking
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
        before=False
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
            doc_list.append({'doc': doc, 'page_nums': doc_pages[doc_id]})
            data_list.append(
                {
                    'src': default_storage.abspath(doc.path),
                    'doc_path': doc.path,
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
        # Important! - first document must inherit metakeys from
        # parent folder
        if parent:
            doc.inherit_kv_from(parent)

        # and only afterwards create pages must be called.
        # create_pages will trigger metadata keys from document
        # to the created pages.
        doc.create_pages()
        # https://github.com/django-mptt/django-mptt/issues/568
        doc._tree_manager.rebuild()

        return doc

    @property
    def absfilepath(self):
        return default_storage.abspath(
            self.path.url()
        )

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
        endpoints:

            page_ep = doc.page_eps[2]
            page_ep.url() # local url to second page of the doc.

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
