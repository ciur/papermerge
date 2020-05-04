import logging
import time

from django.conf import settings
from pmworker import mime
from pmworker.pdfinfo import get_pagecount
from mglib.endpoint import (
    DocumentEp,
    PageEp,
    Endpoint
)
from pmworker.step import (Step, Steps)
from pmworker.shortcuts import (
    extract_img,
    extract_hocr,
    extract_txt
)

logger = logging.getLogger(__name__)


def ocr_page_pdf(
    doc_ep,
    page_num,
    lang
):
    page_count = get_pagecount(doc_ep.url())
    if page_num <= page_count:
        page_url = PageEp(
            document_ep=doc_ep,
            page_num=page_num,
            step=Step(1),
            page_count=page_count
        )
        extract_img(page_url)
        extract_txt(
            page_url,
            lang=lang
        )

        for step in Steps():
            page_url.step = step
            extract_img(page_url)
            # tesseract unterhalt-1.jpg page-1 -l deu hocr
            if not step.is_thumbnail:
                extract_hocr(
                    page_url,
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

    doc_ep = DocumentEp(
        user_id=user_id,
        document_id=document_id,
        file_name=file_name,
        local_endpoint=Endpoint(f"local:/{settings.MEDIA_ROOT}"),
        remote_endpoint=Endpoint("s3:/")
    )

    mime_type = mime.Mime(doc_ep.url())

    page_type = ''
    if mime_type.is_pdf():
        ocr_page_pdf(
            doc_ep=doc_ep,
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
