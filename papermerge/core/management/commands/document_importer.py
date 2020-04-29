import os
import time
from operator import itemgetter
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from papermerge.core.document_importer import DocumentImporter

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Import documents from importer directory
"""

    def add_arguments(self, parser):
        parser.add_argument(
            "directory",
            default=settings.PAPERMERGE_IMPORTER_DIR,
            nargs="?",
            help="The importer directory."
        )

    def main_loop(self, directory):
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

    def handle(self, *args, **options):
        directory = options.get('directory')

        self.main_loop(directory)
