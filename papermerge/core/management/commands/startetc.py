from pathlib import Path
import logging
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand
from django.conf import settings


logger = logging.getLogger(__name__)


class Rundir:
    """
    Sort of context directory
    """
    def __init__(self, proj_root):
        self.proj_root = proj_root

    def exists(self):
        pass

    def create(self):
        pass

    def filepath(self, filename=None):
        pass


def string_to_file(string, filepath, force=False):
    pass


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
        parser.add_argument(
            '--force',
            '-f',
            action="store_true",
            help="Overwrite already existing files"
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        context = self.get_context()

        rundir = Rundir(proj_root=settings.PROJ_ROOT)

        if not rundir.exists():
            rundir.create()

        for file in [
            'etc/nginx.conf',
            'etc/gunicorn.conf.py',
            'etc/systemd/nginx.service',
            'etc/systemd/papermerge.service'
        ]:
            rendered = render_to_string(file, context)
            string_to_file(
                string=rendered,
                filepath=rundir.filepath(filename=file),
                force=force
            )
