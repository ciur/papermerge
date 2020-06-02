import logging

from celery import shared_task
from papermerge.core.ocr.page import ocr_page as main_ocr_page

from .models import Document, Folder, Page

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
    main_ocr_page(
        user_id=user_id,
        document_id=document_id,
        file_name=file_name,
        page_num=page_num,
        lang=lang
    )

    return True


def norm_pages_from_doc(document):
    for page in Page.objects.filter(document=document):
        page.norm()


def norm_pages_from_folder(folder):
    for child in folder.children():
        norm_pages_from_doc(child)


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
