import os
import time
from operator import itemgetter
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from papermerge.core.document_importer import DocumentImporter

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Import documents from importer directory.
    Importer directory is defined by PAPERMERGE_IMPORTER_DIR configuration
    setting.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            "directory",
            default=settings.PAPERMERGE_IMPORTER_DIR,
            nargs="?",
            help="The importer directory."
        )
        parser.add_argument(
            "--loop-time",
            "-t",
            default=settings.PAPERMERGE_IMPORTER_LOOP_TIME,
            type=int,
            help="Wait time between each loop (in seconds)."
        )

    def import_documents(self, directory):
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
                DocumentImporter(file)

    def main_loop(self, directory, loop_time):
        while True:
            start_time = time.time()
            self.import_documents(directory)
            # Sleep until the start of the next loop step
            time.sleep(
                max(0, start_time + loop_time - time.time())
            )

    def handle(self, *args, **options):
        directory = options.get('directory')
        loop_time = options.get('loop_time')
        try:
            self.main_loop(directory, loop_time)
        except KeyboardInterrupt:
            logger.info("Exiting")
