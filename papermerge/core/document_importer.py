import logging

from pmworker.pdfinfo import get_pagecount
from papermege.core.models import (User, Document, Folder)
from papermerge.core.utils import (
    get_root_user,
    get_file_title,
    get_default_language
)

logger = logging.getLogger(__name__)


class DocumentImporter:

    def __init__(self, file, username=None):
        self.filepath = file

        if username is None:
            self.user = get_root_user()
        else:
            self.user = User.objects.first(username=self.username)

        if self.user is None:
            raise Exception("Papermerge has no users defined")

    def import_file(
        self,
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
        logger.info(f"Importing file {self.filepath}")

        if file_title is None:
            file_title = get_file_title(self.filepath)

        lang = get_default_language()
        try:
            page_count = get_pagecount(self.filepath)
        except Exception:
            logger.error(f"File {self.filepath} not yet ready for importing.")
            return False

        inbox, _ = Folder.objects.get_or_create(
            title=inbox_title,
            parent=None,
            user=self.user
        )
        doc = Document.create_document(
            user=self.user,
            title=file_title,
            size=get_file_size(self.filepath),
            lang=lang,
            file_name=file_title,
            parent_id=inbox.id,
            page_count=page_count
        )
        logger.debug(
            f"Uploading file {self.filepath} to {doc.doc_ep.url()}"
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
        )

        Document.ocr_async(
            document=doc,
            page_count=page_count,
            lang=lang,
            s3_enabled=settings.S3
        )

        if delete_after_import:
            os.remove(filepath)

        return doc
