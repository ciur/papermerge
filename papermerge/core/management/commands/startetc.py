import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Generates project etc folder
"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
