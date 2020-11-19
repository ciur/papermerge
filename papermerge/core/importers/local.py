import os
import time
import logging
import tempfile
import shutil

from django.conf import settings
from operator import itemgetter
from django.utils import module_loading

logger = logging.getLogger(__name__)


def import_documents(directory):
    files = []
    pipelines = settings.PAPERMERGE_PIPELINES

    if not directory:
        raise ValueError("Import directory value is None")

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
            basename = os.path.basename(file)
            with tempfile.TemporaryDirectory() as tempdirname:
                shutil.move(file, tempdirname)
                temp_file_name = os.path.join(
                    tempdirname, basename
                )
                logger.info(f"Same as temp_file_name={temp_file_name}...")
                for pipeline in pipelines:
                    pipeline_class = module_loading.import_string(pipeline)
                    importer = pipeline_class(payload=temp_file_name, processor="LOCAL")
                    doc = importer.apply(user=None, name=basename, delete_after_import=True)

