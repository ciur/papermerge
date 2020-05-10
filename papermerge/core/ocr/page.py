import logging
import time

from django.conf import settings
from papermerge.core.storage import default_storage
from pmworker import mime
from pmworker.pdfinfo import get_pagecount
from mglib.path import (
    DocumentPath,
    PagePath,
)
from mglib.step import (Step, Steps)
from mglib.shortcuts import (
    extract_img,
    extract_hocr,
    extract_txt
)

logger = logging.getLogger(__name__)


def ocr_page_pdf(
    doc_path,
    page_num,
    lang
):
    """
    doc_path is an mglib.path.DocumentPath instance
    """
    page_count = get_pagecount(
        default_storage.abspath(doc_path.url())
    )
    if page_num <= page_count:
        page_url = PagePath(
            document_path=doc_path,
            page_num=page_num,
            step=Step(1),
            page_count=page_count
        )
        extract_img(
            page_url,
            media_root=settings.MEDIA_ROOT
        )
        extract_txt(
            page_url,
            lang=lang,
            media_root=settings.MEDIA_ROOT
        )

        for step in Steps():
            page_url.step = step
            extract_img(
                page_url,
                media_root=settings.MEDIA_ROOT
            )
            # tesseract unterhalt-1.jpg page-1 -l deu hocr
            if not step.is_thumbnail:
                extract_hocr(
                    page_url,
                    lang=lang,
                    media_root=settings.MEDIA_ROOT
                )

    return page_url


def ocr_page(
    user_id,
    document_id,
    file_name,
    page_num,
    lang,
):
    logger.debug(
        f" ocr_page user_id={user_id} doc_id={document_id}"
        f" page_num={page_num}"
    )
    t1 = time.time()
    lang = lang.lower()

    doc_path = DocumentPath(
        user_id=user_id,
        document_id=document_id,
        file_name=file_name,
    )

    mime_type = mime.Mime(
        default_storage.abspath(doc_path.url())
    )

    page_type = ''
    if mime_type.is_pdf():
        ocr_page_pdf(
            doc_path=doc_path,
            page_num=page_num,
            lang=lang
        )
        page_type = 'pdf'
    else:
        logger.error(
            f" user_id={user_id}"
            f" doc_id={document_id}"
            f" page_num={page_num} error=Unkown file type"
        )
        return True

    t2 = time.time()
    logger.debug(
        f" user_id={user_id} doc_id={document_id}"
        f" page_num={page_num} page_type={page_type}"
        f" total_exec_time={t2-t1:.2f}"
    )

    return True
