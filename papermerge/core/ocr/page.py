import logging
import time

from papermerge.core.storage import default_storage
from pmworker import mime
from pmworker.pdfinfo import get_pagecount
from mglib.path import (
    DocumentPath,
    PagePath,
)
from pmworker.step import (Step, Steps)
from pmworker.shortcuts import (
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
            default_storage.abspath(page_url)
        )
        extract_txt(
            default_storage.abspath(page_url),
            lang=lang
        )

        for step in Steps():
            page_url.step = step
            extract_img(default_storage.abspath(page_url))
            # tesseract unterhalt-1.jpg page-1 -l deu hocr
            if not step.is_thumbnail:
                extract_hocr(
                    default_storage.abspath(page_url),
                    lang=lang
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
