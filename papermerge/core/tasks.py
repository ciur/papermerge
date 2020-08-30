import logging

from celery import shared_task
from papermerge.core.ocr.page import ocr_page as main_ocr_page
from papermerge.core.ocr import (
    COMPLETE,
    STARTED
)

from .models import Document, Folder, Page
from .utils import Timer
from . import signal_definitions as signals

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def ocr_page(
    self,
    user_id,
    document_id,
    file_name,
    page_num,
    lang,
):
    # A task being bound (bind=True) means the first argument
    # to the task will always be the
    # task instance (self).
    # https://celery.readthedocs.io/en/latest/userguide/tasks.html#bound-tasks
    logger.info(f"task_id={self.request.id}")

    # Inform everybody interested that OCR started
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

        main_ocr_page(
            user_id=user_id,
            document_id=document_id,
            file_name=file_name,
            page_num=page_num,
            lang=lang
        )

    # Inform everybody interested that OCR completed/ended
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

    return True


def norm_pages_from_doc(document):
    logger.debug(f"Normalizing document {document.id}")
    for page in Page.objects.filter(document=document):
        page.norm()


def norm_pages_from_folder(folder):
    for descendent in folder.get_descendants():
        if isinstance(descendent, Document):
            norm_pages_from_doc(descendent)
        elif isinstance(descendent, Folder):
            norm_pages_from_folder(descendent)
        else:
            raise ValueError("Unexpected value for descendent instance")


@shared_task
def normalize_pages(origin):
    """
    Normalize Pages. The normalization was triggered model origin.
    origin can be either a Folder or a Document
    """
    if isinstance(origin, Document):
        norm_pages_from_doc(origin)
    elif isinstance(origin, Folder):
        norm_pages_from_folder(origin)
