import logging

from mglib.step import Step

from .models import Document, Automate
from .storage import default_storage
from .metadata_plugins import get_plugin_by_module_name

logger = logging.getLogger(__name__)


def apply_automates(document_id, page_num):

    logger.debug("apply_automates: Begin.")
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
    hocr = ""
    with open(hocr_path, "r") as f:
        hocr = f.read()

    automates = Automate.objects.filter(user=user)
    # are there automates for the user?
    if automates.count() == 0:
        logger.debug(
            f"No automates for user {user}. Quit."
        )
        return

    # check all automates for given user (the owner of the document)
    for automate in automates:

        if automate.is_a_match(hocr):
            logger.debug(f"Automate {automate} matched document={document}")
            plugin_klass = get_plugin_by_module_name(
                automate.plugin_name
            )
            logger.debug(f"Found plugin module={plugin_klass.__module__}")
            logger.debug(f"len(hocr)=={len(hocr)}")
            automate.apply(
                document=document,
                page_num=page_num,
                hocr=hocr,
                # Notice () - plugin passed is instance of the class
                plugin=plugin_klass()
            )
        else:
            logger.debug(
                f"No match for automate={automate}"
                f" doc_id={document_id} page_num={page_num}"
            )
