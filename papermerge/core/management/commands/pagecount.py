import os
import logging
from django.core.management.base import BaseCommand

from mglib.pdfinfo import get_pagecount

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """
    Calls mglib.pdfinfo.get_pagecount(path) on given file path
    Useful for debugging purposes.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            help="Path to a file on local file system"
        )

    def handle(self, *args, **options):
        file_path = options.get(
            'file_path',
            False
        )

        if not os.path.exists(file_path):
            logger.debug(f"Path {file_path} does not exit. Quit.")
            return

        page_count = get_pagecount(file_path)

        logger.debug(f"Page count={page_count}")
