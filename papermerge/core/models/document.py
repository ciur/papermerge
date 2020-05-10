import subprocess
import os
import logging

from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.urls import reverse

from django.utils.translation import ugettext_lazy as _

from mglib.path import (DocumentPath, PagePath)
from mglib import ocrmigrate
from pmworker.pdfinfo import get_pagecount
from pmworker import pdftk


from papermerge.core import mixins
from papermerge.core.models.node import BaseTreeNode
from papermerge.core.models.folder import Folder

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
