import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from papermerge.core.models import Document

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

    def handle(self, *args, **options):
        directory = options.get('directory')

        self.import_documents(
            directory=directory
        )
