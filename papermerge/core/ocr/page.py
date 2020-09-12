import logging
import time

from django.conf import settings
from papermerge.core.storage import default_storage
from mglib import mime
from mglib.pdfinfo import get_pagecount
from mglib.path import (
    DocumentPath,
    PagePath,
)
from mglib.step import (Step, Steps)
from mglib.shortcuts import (
    extract_img,
    resize_img,
    extract_hocr,
    extract_txt,
)
from mglib.tiff import convert_tiff2pdf

logger = logging.getLogger(__name__)

STARTED = "started"
COMPLETE = "complete"


def ocr_page_pdf(
    doc_path,
    page_num,
    lang
):
    """
    doc_path is an mglib.path.DocumentPath instance
    """
    logger.debug("OCR PDF document")

    page_count = get_pagecount(
        default_storage.abspath(doc_path.url())
    )

    if page_num <= page_count:
        # first quickly generate preview images
        page_url = PagePath(
            document_path=doc_path,
            page_num=page_num,
            step=Step(1),
            page_count=page_count
        )
        for step in Steps():
            page_url.step = step
            extract_img(
                page_url,
                media_root=settings.MEDIA_ROOT
            )

    if page_num <= page_count:
        page_url = PagePath(
            document_path=doc_path,
            page_num=page_num,
            step=Step(1),
            page_count=page_count
        )
        extract_txt(
            page_url,
            lang=lang,
            media_root=settings.MEDIA_ROOT
        )

        for step in Steps():
            page_url.step = step
            if not step.is_thumbnail:
                extract_hocr(
                    page_url,
                    lang=lang,
                    media_root=settings.MEDIA_ROOT
                )

    return page_url


def ocr_page_image(
    doc_path,
    page_num,
    lang
):
    """
    image = jpg, jpeg, png
    """
    logger.debug("OCR image (jpeg, jpg, png) document")

    page_url = PagePath(
        document_path=doc_path,
        page_num=page_num,
        step=Step(1),
        # jpeg, jpg, png are 1 page documents
        page_count=1
    )
    # resize and eventually convert (png -> jpg)
    resize_img(
        page_url,
        media_root=settings.MEDIA_ROOT
    )
    extract_txt(
        page_url,
        lang=lang,
        media_root=settings.MEDIA_ROOT
    )

    # First quickly generate preview images
    for step in Steps():
        page_url.step = step
        resize_img(
            page_url,
            media_root=settings.MEDIA_ROOT
        )
    # reset page's step
    page_url.step = Step(1)
    # Now OCR each image
    for step in Steps():
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
    logger.debug(f"Mime Type = {mime_type}")

    page_type = ''

    if mime_type.is_pdf():
        ocr_page_pdf(
            doc_path=doc_path,
            page_num=page_num,
            lang=lang
        )
        page_type = 'pdf'
    elif mime_type.is_image():  # jpeg, jpeg or png
        ocr_page_image(
            doc_path=doc_path,
            page_num=page_num,
            lang=lang
        )
    elif mime_type.is_tiff():
        # new filename is a pdf file
        logger.debug("TIFF type detected")
        new_filename = convert_tiff2pdf(
            doc_url=default_storage.abspath(doc_path.url())
        )
        # now .pdf
        doc_path.file_name = new_filename
        # and continue as usual
        ocr_page_pdf(
            doc_path=doc_path,
            page_num=page_num,
            lang=lang
        )
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
