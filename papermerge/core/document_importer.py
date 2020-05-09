import os
import logging

from pmworker.pdfinfo import get_pagecount
from papermerge.core.models import (User, Document, Folder)
from papermerge.core.utils import get_superuser
from papermerge.core.ocr import ocr_page
from pmworker.storage import copy2doc_url

logger = logging.getLogger(__name__)


class DocumentImporter:

    def __init__(self, file, username=None):
        self.filepath = file

        if username is None:
            self.user = get_superuser()
        else:
            self.user = User.objects.first(username=self.username)

        if self.user is None:
            raise Exception("Papermerge has no users defined")

    @property
    def user_ocr_language(self):
        return self.user.preferences['ocr__OCR_Language']

    def import_file(
        self,
        file_title=None,
        inbox_title="Inbox",
        delete_after_import=True
    ):
        """
        Gets as input a path to a file on a local file system and:
            1. creates a document instance
            2. Copies file to doc_instance.url()
            4. OCR the doc

        Used with
            ./manage.py local_importer
            ./manage.py imap_importer
        command
        """
        logger.info(f"Importing file {self.filepath}")

        if file_title is None:
            file_title = os.path.basename(self.filepath)

        try:
            page_count = get_pagecount(self.filepath)
        except Exception:
            logger.error(f"Error while getting page count of {self.filepath}.")
            return False

        inbox, _ = Folder.objects.get_or_create(
            title=inbox_title,
            parent=None,
            user=self.user
        )
        doc = Document.create_document(
            user=self.user,
            title=file_title,
            size=os.path.getsize(self.filepath),
            lang=self.user_ocr_language,
            file_name=file_title,
            parent_id=inbox.id,
            page_count=page_count
        )
        logger.debug(
            f"Uploading file {self.filepath} to {doc.doc_ep.url()}"
        )
        copy2doc_url(
            src_file_path=self.filepath,
            doc_url=doc.doc_ep.url(),
        )

        DocumentImporter.ocr_document(
            document=doc,
            page_count=page_count,
            lang=self.user_ocr_language,
        )

        if delete_after_import:
            # Usually we want to delete files when importing
            # them from local directory
            # When importing from Email attachment - deleting
            # files does not apply
            os.remove(self.filepath)

        logger.debug("Import complete.")

        return doc

    @classmethod
    def ocr_document(
        cls,
        document,
        page_count,
        lang,
    ):
        user_id = document.user.id
        document_id = document.id
        file_name = document.file_name
        logger.debug(f"Document {document_id} has {page_count} pages")
        for page_num in range(1, page_count + 1):
            ocr_page(
                user_id=user_id,
                document_id=document_id,
                file_name=file_name,
                page_num=page_num,
                lang=lang
            )
            document.save()
