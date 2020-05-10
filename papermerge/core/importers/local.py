import os
import time
import logging
from django.conf import settings
from operator import itemgetter
from papermerge.core.document_importer import DocumentImporter

logger = logging.getLogger(__name__)


def import_documents(directory):
    files = []
    for entry in os.scandir(directory):
        if entry.is_file():
            file = (entry.path, entry.stat().st_mtime)
            files.append(file)
        else:
            logger.warning(
                "Skipping %s as it is not a file",
                entry.path
            )

    if not files:
        return

    files_old_to_new = sorted(files, key=itemgetter(1))

    time.sleep(int(settings.PAPERMERGE_FILES_MIN_UNMODIFIED_DURATION))

    for file, mtime in files_old_to_new:
        if mtime == os.path.getmtime(file):
            # File has not been modified and can be consumed
            logger.info(f"Importing file {file}...")
            imp = DocumentImporter(file)
            imp.import_file()
