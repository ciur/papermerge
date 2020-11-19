from os.path import getsize, basename
import logging
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.core.exceptions import ValidationError

from papermerge.core.models import (
    Folder, Document, User
)
from papermerge.core.storage import default_storage
from papermerge.core.tasks import ocr_page

from mglib.pdfinfo import get_pagecount
from magic import from_file

logger = logging.getLogger(__name__)

class DefaultPipeline:
    def __init__(self, payload, processor="WEB"):
        if processor == "IMAP":
            try:
                self.payload = payload.get_payload(decode=True)
            except TypeError as e:
                logger.debug("{} importer: not a file.".format(processor))
        else:
            self.tempfile = payload

        self.processor = processor

    def check_mimetype(self):
        """
        Check if mimetype of the document to be imported is supported
        by Papermerge or one of its apps.
        """
        supported_mimetypes = settings.PAPERMERGE_MIMETYPES
        mime = from_file(self.tempfile.temporary_file_path(), mime=True)
        if mime in supported_mimetypes:
            return True
        return False
   
    def write_temp(self):
        logger.debug("{} importer: creating temporary file".format(self.processor))
        temp = NamedTemporaryFile()
        temp.write(self.payload)
        temp.flush()
        self.tempfile = temp
        return

    @staticmethod
    def get_user_properties(user):
        if user is None:
            user = User.objects.filter(
                       is_superuser=True
                   ).first()
        lang = user.preferences['ocr__OCR_Language']
        inbox, _ = Folder.objects.get_or_create(
                       title=Folder.INBOX_NAME,
                       parent=None,
                       user=user
                   )
        return user, lang, inbox

    def move_tempfile(self, doc):
        default_storage.copy_doc(
            src=self.tempfile.temporary_file_path(),
            dst=doc.path.url()
        )
        return

    def page_count(self):
        return get_pagecount(self.tempfile.temporary_file_path())

    @staticmethod
    def ocr_document(
        document,
        page_count,
        lang,
    ):
        user_id = document.user.id
        document_id = document.id
        file_name = document.file_name
        logger.debug("{} importer: document {} has {} pages.".format(self.processor, document_id, page_count))
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

            msg = "{} importer: OCR took {} seconds to complete.".format(self.processor, time)
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

    def apply(self, user=None, parent=None, lang=None, 
              notes=None, name=None, skip_ocr=False, 
              apply_async=False, delete_after_import=False):
        if not self.check_mimetype():
            logger.debug("{} importer: invalid filetype".format(self.processor))
            return None
        if self.processor != "WEB":
            user, lang, inbox = self.get_user_properties(user)
            parent = inbox.id
        if name is None:
            name = basename(self.tempfile.name)
        page_count = self.page_count()
        size = getsize(self.tempfile.temporary_file_path())
        try:
            doc = Document.objects.create_document(
                      user=user,
                      title=name,
                      size=size,
                      lang=lang,
                      file_name=name,
                      parent_id=parent,
                      page_count=page_count,
                      notes=notes
                  )
        except ValidationError as e:
            logger.error("{} importer: validation failed".format(self.processor))
            return None
        self.move_tempfile(doc)
        self.tempfile.close()
        if not skip_ocr:
            if apply_async:
                for page_num in range(1, page_count + 1):
                    ocr_page.apply_async(kwargs={
                        'user_id': user.id,
                        'document_id': doc.id,
                        'file_name': name,
                        'page_num': page_num,
                        'lang': lang}
                    )
            else:
                ocr_document(
                    document=doc,
                    page_count=page_count,
                    lang=lang,
                )

        if delete_after_import:
            os.remove(self.tempfile)

        logger.debug("{} importer: import complete.".format(self.processor))
        return doc

