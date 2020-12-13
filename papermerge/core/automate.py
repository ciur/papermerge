import logging

from django.utils.translation import gettext as _

from mglib.step import Step
from mglib.path import PagePath, DocumentPath
from mglib.pdfinfo import get_pagecount

from .models import Document, Automate
from .storage import default_storage
from .signal_definitions import automates_matching


logger = logging.getLogger(__name__)


def apply_automates(document_id, page_num):

    logger.debug("apply_automates: Begin.")
    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        logger.error(f"Provided document_id={document_id}, does not exists")
        return

    # use text files from the original version of the document
    doc_path = DocumentPath.copy_from(
        document.path(),
        version=0
    )
    page_count = get_pagecount(
        default_storage.abspath(doc_path.url())
    )
    page_path = PagePath(
        document_path=doc_path,
        page_num=page_num,
        page_count=page_count,
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

            automate.apply(
                document=document,
                page_num=page_num,
                text=text,
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
        document_id=document_id,
        level=logging.INFO,
        message=message,
        page_num=page_num,
        text=text
    )
