import logging
import time

from pmworker import mime
from pmworker.pdfinfo import get_pagecount
from pmworker.endpoint import (
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
from pmworker import (
    get_local_storage_root_url,
    get_s3_storage_root_url
)

logger = logging.getLogger(__name__)


def ocr_page_pdf(
    doc_ep,
    page_num,
    lang
):
    page_count = get_pagecount(doc_ep.url())
    logger.debug(f"page_count={page_count}")
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
    # A task being bound (bind=True) means the first argument
    # to the task will always be the
    # task instance (self).
    # https://celery.readthedocs.io/en/latest/userguide/tasks.html#bound-tasks
    logger.info(
        f" user_id={user_id} doc_id={document_id}"
        f" page_num={page_num}"
    )
    t1 = time.time()
    lang = lang.lower()

    doc_ep = DocumentEp(
        user_id=user_id,
        document_id=document_id,
        file_name=file_name,
        local_endpoint=get_local_storage_root_url(),
        remote_endpoint=get_s3_storage_root_url()
    )

    logger.debug(
        f"Received document_url={doc_ep.url(Endpoint.S3)}"
    )

    mime_type = mime.Mime(doc_ep.url())

    page_type = ''
    if mime_type.is_pdf():
        tx1 = time.time()
        ocr_page_pdf(
            doc_ep=doc_ep,
            page_num=page_num,
            lang=lang
        )
        page_type = 'pdf'
        tx2 = time.time()
        logger.info(
            f" user_id={user_id}"
            f" doc_id={document_id}"
            f" page_num={page_num} page_type=pdf page_ocr_time={tx2-tx1:.2f}"
        )
    else:
        logger.info(
            f" user_id={user_id}"
            f" doc_id={document_id}"
            f" page_num={page_num} error=Unkown file type"
        )
        return True

    t2 = time.time()
    logger.info(
        f" user_id={user_id} doc_id={document_id}"
        f" page_num={page_num} page_type={page_type}"
        f" total_exec_time={t2-t1:.2f}"
    )

    return True
