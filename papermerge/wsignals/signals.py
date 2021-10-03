import logging
from django.dispatch import receiver
from django.utils.translation import gettext as _

from papermerge.core.signal_definitions import (
    page_ocr,
    automates_matching,
    WORKER
)
from papermerge.core.models import Document
from papermerge.core.ocr import COMPLETE
from papermerge.core.automate import apply_automates


logger = logging.getLogger(__name__)

# All below handlers are sent from the worker instance.
# Notice that worker must have access to same DB as webapp
# which might not always be the case


@receiver(page_ocr, sender=WORKER)
def apply_automates_handler(sender, **kwargs):
    """
    Signal sent by the worker when HOCR file is ready i.e.
    OCR for page is complete.

    Important! Worker can be deployed on separate computer
    as webapp. In such case, django signals sent by the worker instance
    will not reach webapp.
    """
    document_id = kwargs.get('document_id', False)
    page_num = kwargs.get('page_num', False)
    status = kwargs.get('status')

    if status == COMPLETE:
        logger.debug(
            f"Page hocr ready: document_id={document_id} page_num={page_num}"
        )
        try:
            # will hit the database
            apply_automates(
                document_id=document_id,
                page_num=page_num
            )
        except Exception as e:
            logger.error(f"Exception {e} in apply_automates_handler.")
            raise


@receiver(automates_matching)
def automates_matching_handler(sender, **kwargs):
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')
    doc_id = kwargs.get('document_id')
    message = kwargs.get('message')
    page_num = kwargs.get('page_num')
    text = kwargs.get('text')

    try:
        # will hit the database
        doc = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        try:
            # documment was not found, add this logging
            # information to UI logs as well.
            msg = _(
                "Running automates for doc_id=%(doc_id)s,"
                " page %(page_num)s."
                "But in meantime document probably was deleted."
            ) % {
                'doc_id': doc_id,
                'page_num': page_num
            }
            logger.warning(msg)
            return
        except Exception as e:
            logger.error(
                f"Exception {e} in during automates_matching_handler. "
            )
            raise

    document_title = doc.title

    log_entry_message = _(
        "Running automates for document %(document_title)s, page=%(page_num)s,"
        " doc_id=%(doc_id)s. text=%(text)s"
    ) % {
        'document_title': document_title,
        'page_num': page_num,
        'doc_id': doc_id,
        'text': text
    }

    log_entry_message += message


@receiver(page_ocr)
def page_ocr_handler(sender, **kwargs):
    """
    Nicely log starting/completion of OCRing of each page
    """
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')
    doc_id = kwargs.get('document_id')
    message = kwargs.get('message')
    page_num = kwargs.get('page_num')
    lang = kwargs.get('lang')
    status = kwargs.get('status')

    if status == COMPLETE:
        human_status = _("COMPLETE")
    else:
        human_status = _("STARTED")

    try:
        # will hit the database
        doc = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        try:
            msg = _(
                "%(human_status)s OCR for doc_id=%(doc_id)s,"
                " page %(page_num)s."
                "But in meantime document probably was deleted."
            ) % {
                'human_status': human_status,
                'doc_id': doc_id,
                'page_num': page_num
            }
            logger.warning(msg)
            return
        except Exception as e:
            logger.error(
                f"Exception {e} during handling of page_ocr_handler"
            )
            raise

    document_title = doc.title

