import logging

from django.dispatch import receiver
from django.utils.translation import gettext as _

from papermerge.core.models import Folder, Document

from papermerge.core.signal_definitions import (
    folder_created,
    nodes_deleted,
    page_ocr
)
from papermerge.core.utils import node_tag
from papermerge.contrib.admin.models import LogEntry
from papermerge.core.ocr import (
    COMPLETE,
    STARTED
)


@receiver(page_ocr)
def page_ocr_handler(sender, **kwargs):
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')
    doc_id = kwargs.get('document_id')
    message = kwargs.get('message')
    page_num = kwargs.get('page_num')
    lang = kwargs.get('lang')
    status = kwargs.get('status')

    if status == COMPLETE:
        human_status = _("complete")
    else:
        human_status = _("started")

    try:
        doc = Document.object.get(id=doc_id)
    except Document.DoesNotExist:
        LogEntry.objects.create(
            user_id=user_id,
            level=logging.WARGNING,
            message=_(
                f"OCR {human_status} for doc_id={doc_id}, page {page_num}."
                f"But in meantime document probably was deleted"
            )
        )

        return

    doc_tag = node_tag(doc)

    log_entry_message = ""

    if status == STARTED:
        log_entry_message = _(
            f"OCR {human_status} for document {doc_tag}, page {page_num}."
            f" language={lang} "
        )
    elif status == COMPLETE:
        log_entry_message = _(
            f"OCR {human_status} for document {doc_tag}, page {page_num}."
            f" language={lang}. "
        )
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

    folder_tag = node_tag(folder)

    msg = f"Node/Folder {folder_tag} created."

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )


@receiver(nodes_deleted)
def nodes_deleted_handler(sender, **kwargs):
    node_tags = kwargs.get('node_tags')
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')

    msg = f"Node(s) {','.join(node_tags)} were deleted."

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )
