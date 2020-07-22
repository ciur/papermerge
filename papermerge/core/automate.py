import logging

from mglib.step import Step

from .models import Document, Automate
from .storage import default_storage
from .metadata_plugins import get_plugin_by_module_name

logger = logging.getLogger(__name__)


def apply_automates(document_id, page_num):

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        logger.error(f"Provided document_id={document_id}, does not exists")
        return

    page_path = document.get_page_path(
        page_num=page_num,
        step=Step(),
    )
    user = document.user
    hocr_path = default_storage.abspath(page_path.hocr_url())

    # check all automates for given user (the owner of the document)
    for automate in Automate.objects.filter(user=user):

        if automate.is_a_match(hocr_path):
            logger.debug(f"Automate {automate} matched document={document}")
            plugin = get_plugin_by_module_name(
                automate.plugin_name
            )
            automate.apply(
                document,
                page_num,
                hocr_path,
                plugin
            )
