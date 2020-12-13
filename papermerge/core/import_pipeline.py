import os
from os.path import getsize, basename
import logging
from email.message import Message

from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.core.exceptions import ValidationError

from papermerge.core.models import (
    Folder, Document, User
)
from papermerge.core.storage import default_storage
from papermerge.core.tasks import ocr_page
from papermerge.core import signal_definitions as signals
from papermerge.core.ocr import COMPLETE, STARTED
from papermerge.core.utils import Timer

from mglib.pdfinfo import get_pagecount
from magic import from_file

logger = logging.getLogger(__name__)


# 3 types of import_pipelines
WEB = "WEB"
IMAP = "IMAP"
LOCAL = "LOCAL"


class DefaultPipeline:
    """
    Please document:
        1. What is a pipeline?
        2. What are usecases?
        3. What functions are mandatory?
        4. Examples
    """

    def __init__(
        self,
        payload,
        doc=None,
        processor=WEB,
        *args,
        **kwargs
    ):

        if payload is None:
            return None

        self.processor = processor
        self.doc = doc
        self.name = None

        if isinstance(payload, Message):
            try:
                payload = payload.get_payload(decode=True)
                if payload is None:
                    logger.debug("{} importer: not a file.".format(processor))
                    raise TypeError("Not a file.")
                self.write_temp(payload)
            except TypeError as e:
                logger.debug("{} importer: not a file.".format(processor))
                raise e
        else:
            self.tempfile = payload

        if doc is not None:
            self.temppath = self.tempfile.name
        elif processor == WEB:
            self.temppath = self.tempfile.temporary_file_path()

    def check_mimetype(self):
        """
        Check if mimetype of the document to be imported is supported
        by Papermerge or one of its apps.
        """
        supported_mimetypes = settings.PAPERMERGE_MIMETYPES
        mime = from_file(self.temppath, mime=True)
        if mime in supported_mimetypes:
            return True
        return False

    def write_temp(self, payload):
        """
        What is this function doing?
        When is this function used ?
        """
        logger.debug(
            f"{self.processor} importer: creating temporary file"
        )

        temp = NamedTemporaryFile()
        temp.write(payload)
        temp.flush()
        self.tempfile = temp
        self.temppath = temp.name
        # does this return have a purpose?
        # is this function supposed to return something?
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
            src=self.temppath,
            dst=doc.path().url()
        )
        return

    def page_count(self):
        return get_pagecount(self.temppath)

    def ocr_document(
        self,
        document,
        page_count,
        lang
    ):

        user_id = document.user.id
        document_id = document.id
        file_name = document.file_name

        logger.debug(
            f"{self.processor} importer: "
            f"document {document_id} has {page_count} pages."
        )
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

            msg = "{} importer: OCR took {} seconds to complete.".format(
                self.processor,
                time
            )
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

    def get_init_kwargs(self):
        """
        Is this function supposed to return something?
        Please document
        """
        if self.doc:
            return {'doc': self.doc}
        return None

    def get_apply_kwargs(self):
        """
        Is this function supposed to return something?
        Please document
        """
        if self.doc:
            return {'doc': self.doc}
        return None

    def apply(
        self,
        user=None,
        parent=None,
        lang=None,
        notes=None,
        name=None,
        skip_ocr=False,
        apply_async=False,
        delete_after_import=False,
        create_document=True,
        *args,
        **kwargs
    ):
        """
        Is this function supposed to return something ?
        Please document.
        """
        if not self.check_mimetype():
            logger.debug(
                f"{self.processor} importer: invalid filetype"
            )
            return None
        if self.processor != WEB:
            user, lang, inbox = self.get_user_properties(user)
            parent = inbox.id
        if name is None:
            name = basename(self.tempfile.name)
        page_count = self.page_count()
        size = getsize(self.temppath)

        if create_document:
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
                self.doc = doc
            except ValidationError as e:
                logger.error(
                    "{} importer: validation failed".format(self.processor)
                )
                raise e
        elif self.doc is not None:
            doc = self.doc
            doc.version = doc.version + 1
            doc.page_count = page_count
            doc.file_name = name
            doc.save()
            try:
                doc.recreate_pages()
            except ValueError:
                doc.create_pages()
            except Exception:
                logger.error(
                    f"{self.processor} importer: could not create pages"
                )

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
                self.ocr_document(
                    document=doc,
                    page_count=page_count,
                    lang=lang,
                )

        if delete_after_import:
            os.remove(self.temppath)

        logger.debug("{} importer: import complete.".format(self.processor))
        return {
            'doc': doc
        }
