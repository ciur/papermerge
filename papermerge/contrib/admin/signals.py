import logging

from django.dispatch import receiver
from django.utils.translation import gettext as _

from papermerge.core.models import (
    Folder,
    Document
)

from papermerge.core.signal_definitions import (
    automates_matching,
    folder_created,
    nodes_deleted,
    page_ocr
)
from papermerge.contrib.admin.models import LogEntry
from papermerge.core.ocr import COMPLETE

logger = logging.getLogger(__name__)


@receiver(automates_matching)
def automates_matching_handler(sender, **kwargs):
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')
    doc_id = kwargs.get('document_id')
    message = kwargs.get('message')
    page_num = kwargs.get('page_num')
    text = kwargs.get('text')

    try:
        doc = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        LogEntry.objects.create(
            user_id=user_id,
            level=logging.WARNING,
            message=_(
                "Running automates for doc_id=%(doc_id)s,"
                " page %(page_num)s."
                "But in meantime document probably was deleted."
            ) % {
                'doc_id': doc_id,
                'page_num': page_num
            }
        )
        return

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

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=log_entry_message
    )


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
        doc = Document.objects.get(id=doc_id)
    except Document.DoesNotExist:
        LogEntry.objects.create(
            user_id=user_id,
            level=logging.WARNING,
            message=_(
                "%(human_status)s OCR for doc_id=%(doc_id)s,"
                " page %(page_num)s."
                "But in meantime document probably was deleted."
            ) % {
                'human_status': human_status,
                'doc_id': doc_id,
                'page_num': page_num
            }
        )
        return

    document_title = doc.title

    log_entry_message = _(
        "%(human_status)s OCR for document %(document_title)s,"
        " page=%(page_num)s,"
        " language=%(lang)s, doc_id=%(doc_id)s."
    ) % {
        'human_status': human_status,
        'document_title': document_title,
        'page_num': page_num,
        'lang': lang,
        'doc_id': doc_id,
    }

    if status == COMPLETE:
        # for COMPLETE sinals message argument
        # contains a line with time it took to OCR the document.
        log_entry_message += message

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=log_entry_message
    )


@receiver(folder_created)
def folder_created_handler(sender, **kwargs):
    folder_id = kwargs.get('folder_id')
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')

    folder = Folder.objects.get(id=folder_id)

    folder_title = folder.title

    msg = _(
        "Node/Folder %(folder_title)s created. Folder id=%(folder_id)s."
    ) % {
        'folder_title': folder_title,
        'folder_id': folder_id
    }

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )


@receiver(nodes_deleted)
def nodes_deleted_handler(sender, **kwargs):
    node_titles = kwargs.get('node_titles')
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')
    node_ids = kwargs.get('node_ids')
    msg = _(
        "Node(s) %(node_titles)s were deleted. Node ids=%(node_ids)s"
    ) % {
        'node_titles': ', '.join(node_titles),
        'node_ids': node_ids
    }

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )
