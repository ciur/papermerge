import logging
from django.core.management.base import BaseCommand

from papermerge.core.automate import apply_automates

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """
    Triggers core.automate.apply_automates(document_id, page_num).
    Useful for debugging purposes.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            'document_id',
            type=int,
            help="Document id passed as argument to apply_automates function"
        )
        parser.add_argument(
            'page_num',
            type=int,
            help="page_num passed as argument to apply_automates function."
        )

    def handle(self, *args, **options):
        document_id = options.get(
            'document_id',
            False
        )
        page_num = options.get(
            'page_num',
            False
        )

        apply_automates(document_id, page_num)
