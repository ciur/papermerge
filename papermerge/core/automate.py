import logging

from django.utils.translation import gettext as _

from mglib.step import Step

from .models import Document, Automate
from .storage import default_storage
from .metadata_plugins import get_plugin_by_module_name
from .signal_definitions import automates_matching

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

    text_path = default_storage.abspath(page_path.txt_url())
    text = ""
    with open(text_path, "r") as f:
        text = f.read()

    automates = Automate.objects.filter(user=user)
    # are there automates for the user?
    if automates.count() == 0:
        logger.debug(
            f"No automates for user {user}. Quit."
        )
        return

    # check all automates for given user (the owner of the document)
    matched = []
    for automate in automates:
        if automate.is_a_match(text):
            logger.debug(f"Automate {automate} matched document={document}")

            plugin_klass = get_plugin_by_module_name(
                automate.plugin_name
            )
            plugin = plugin_klass() if plugin_klass else None

            automate.apply(
                document=document,
                page_num=page_num,
                hocr=text,
                # Notice () - plugin passed is instance of the class
                plugin=plugin
            )
            matched.append(automate)
        else:
            logger.debug(
                f"No match for automate={automate}"
                f" doc_id={document_id} page_num={page_num}"
            )

    message = ""

    message = _(
        "%(count)s of %(total)s Automate(s) matched. ") % {
        'count': len(matched),
        'total': automates.count()
    }

    if len(matched) > 0:
        message += _("List of matched Automates: %(matched_automates)s") % {
            'matched_automates': matched
        }

    automates_matching.send(
        sender="papermerge.core.automate",
        user_id=document.user.id,
        level=logging.INFO,
        message=message,
        page_num=page_num,
        text=text
    )
