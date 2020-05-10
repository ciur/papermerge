import time
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from papermerge.core.importers.imap import import_attachment
from papermerge.core.importers.local import import_documents


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Import documents from email attachments and
    from local folder.
    importer = imap_importer + local_importer
"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--loop-time",
            "-t",
            default=settings.PAPERMERGE_IMPORTER_LOOP_TIME,
            type=int,
            help="Wait time between each loop (in seconds)."
        )
        parser.add_argument(
            "directory",
            default=settings.PAPERMERGE_IMPORTER_DIR,
            nargs="?",
            help="The importer directory."
        )

    def main_loop(self, directory, loop_time):
        while True:
            start_time = time.time()
            import_attachment()  # imap importer
            import_documents(directory)  # local importer
            # Sleep until the start of the next loop step
            time.sleep(
                max(0, start_time + loop_time - time.time())
            )

    def handle(self, *args, **options):
        loop_time = options.get('loop_time')
        directory = options.get('directory')

        try:
            self.main_loop(directory, loop_time)
        except KeyboardInterrupt:
            logger.info("Exiting")
