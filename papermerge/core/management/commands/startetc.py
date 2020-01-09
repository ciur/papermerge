import logging
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand
from django.conf import settings


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Generates project etc folder
"""

    def get_context(self):
        context = {
            'proj_root': settings.PROJ_ROOT,
            'static_root': settings.STATIC_ROOT
        }
        return context

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        context = self.get_context()
        rendered = render_to_string('etc/nginx.conf', context)
        print(rendered)
