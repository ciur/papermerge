import logging

from django.core.management.base import BaseCommand
from papermerge.core.metadata_plugins import apply_metadata_plugins

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """
    Run metadata plugin on specific document_id/page_num
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "document_id",
            type=int,
            help="document_id."
        )
        parser.add_argument(
            "page_num",
            type=int,
            help="page_num"
        )

    def handle(self, *args, **options):
        document_id = options.get('document_id')
        page_num = options.get('page_num')

        result = apply_metadata_plugins(
            document_id=document_id,
            page_num=page_num
        )

        print(result)
