import logging
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from papermerge.core.importers.local import import_documents

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

    def main_loop(self, directory, loop_time):
        while True:
            start_time = time.time()
            import_documents(directory)
            # Sleep until the start of the next loop step
            time.sleep(
                max(0, start_time + loop_time - time.time())
            )

    def handle(self, *args, **options):
        directory = options.get('directory')
        loop_time = options.get('loop_time')

        logger.info(f"Watching for files in {directory}...")

        try:
            self.main_loop(directory, loop_time)
        except KeyboardInterrupt:
            logger.info("Exiting")
