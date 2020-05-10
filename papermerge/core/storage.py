import os
import logging
import shutil
from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def copy2doc_url(
    src_file_path,
    dst_file_path
):
    dirname = os.path.dirname(dst_file_path)

    if not os.path.exists(
        dirname
    ):
        os.makedirs(
            dirname, exist_ok=True
        )
    logger.debug(
        f"copy2doc_url {src_file_path} to {dst_file_path}"
    )
    shutil.copyfile(
        src_file_path,
        dst_file_path
    )


def get_storage_class(import_path=None):
    return import_string(
        import_path or settings.PAPERMERGE_DEFAULT_FILE_STORAGE
    )


storage_class = get_storage_class()


default_storage = storage_class()
