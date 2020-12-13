import logging
import os

from .models import Document, Folder, User
from .ocr.page import ocr_page
from papermerge.core.tasks import ocr_page as ocr_page_task
from .utils import Timer
from .storage import default_storage
from .ocr import (
    COMPLETE,
    STARTED
)
from . import signal_definitions as signals

from mglib.pdfinfo import get_pagecount

logger = logging.getLogger(__name__)


class DocumentImporter:

    def __init__(self, file, username=None):
        self.filepath = file

        if username is None:
            # get superuser
            self.user = User.objects.filter(
                is_superuser=True
            ).first()
        else:
            self.user = User.objects.filter(
                username=username
            ).first()

        if self.user is None:
            raise Exception("Papermerge has no users defined")

    @property
    def user_ocr_language(self):
        return self.user.preferences['ocr__OCR_Language']

    def import_file(
        self,
        file_title=None,
        inbox_title=Folder.INBOX_NAME,
        delete_after_import=True,
        skip_ocr=False,
        apply_async=False
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
        logger.debug(f"Importing file {self.filepath}.")

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
        doc = Document.objects.create_document(
            user=self.user,
            title=file_title,
            size=os.path.getsize(self.filepath),
            lang=self.user_ocr_language,
            file_name=file_title,
            parent_id=inbox.id,
            page_count=page_count,
        )
        logger.debug(
            f"Uploading file {self.filepath} to {doc.path().url()}"
        )
        default_storage.copy_doc(
            src=self.filepath,
            dst=doc.path().url(),
        )

        if not skip_ocr:
            if apply_async:
                for page_num in range(1, page_count + 1):
                    ocr_page_task.apply_async(kwargs={
                        'user_id': self.user.id,
                        'document_id': doc.id,
                        'file_name': file_title,
                        'page_num': page_num,
                        'lang': self.user_ocr_language}
                    )
            else:
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
            signals.page_ocr.send(
                sender='worker',
                level=logging.INFO,
                message="",
                user_id=user_id,
                document_id=document_id,
                page_num=page_num,
                lang=lang,
                status=STARTED
            )

            with Timer() as time:
                ocr_page(
                    user_id=user_id,
                    document_id=document_id,
                    file_name=file_name,
                    page_num=page_num,
                    lang=lang,
                )

            msg = f"Ocr took {time} seconds to complete."
            signals.page_ocr.send(
                sender='worker',
                level=logging.INFO,
                message=msg,
                user_id=user_id,
                document_id=document_id,
                page_num=page_num,
                lang=lang,
                status=COMPLETE
            )
