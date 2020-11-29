import os
import time
import logging
from hashlib import blake2b

from django.conf import settings

from papermerge.core.import_pipeline import LOCAL, go_through_pipelines

logger = logging.getLogger(__name__)


def import_documents(directory, skip_ocr=False):
    files = []

    if not directory:
        raise ValueError("Import directory value is None")

    for entry in os.scandir(directory):
        if entry.is_file():
            with open(entry.path, 'rb') as file_handler:
                file_hash = blake2b()
                file_bytes = file_handler.read()
                file_hash.update(file_bytes)
            file_tuple = (entry.path, file_hash.digest())
            files.append(file_tuple)
        else:
            logger.warning(
                "Skipping %s as it is not a file",
                entry.path
            )

    if not files:
        return

    time.sleep(int(settings.PAPERMERGE_FILES_MIN_UNMODIFIED_DURATION))

    for file_path, file_hash in files:
        with open(file_path, 'rb') as file_handler:
            file_bytes = file_handler.read()
            file_hash_new = blake2b()
            file_hash_new.update(file_bytes)
            if not file_hash == file_hash_new.digest():
                continue
            # File has not been modified and can be consumed
            basename = os.path.basename(file_path)
            init_kwargs = {'payload': file_bytes, 'processor': LOCAL}
            apply_kwargs = {'user': None,
                            'name': basename,
                            'skip_ocr': skip_ocr
                            }
            doc = go_through_pipelines(init_kwargs, apply_kwargs)
            if doc is not None:
                os.remove(file_path)
