import sys
import os
from pathlib import Path
import logging
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand
from django.conf import settings


logger = logging.getLogger(__name__)


NOTICE = """# This file was generated using ./manage.py startetc command.
# if you add changes here manually, your changes might be overwritten.
#
# To adjust generated file, have a look at config/templates/etc files.
"""


class Rundir:
    """
    Sort of context directory
    """

    def __init__(self, proj_root):
        self.proj_root = proj_root
        self.proj_run = self.proj_root / Path("run")
        self.proj_etc = self.proj_root / Path("run") / Path("etc")
        self.proj_log = self.proj_root / Path("run") / Path("log")
        self.proj_tmp = self.proj_root / Path("run") / Path("tmp")
        self.proj_systemd = self.proj_etc / Path("systemd")

    def exists(self):
        all_run_dirs = [
            self.proj_root.exists(),
            self.proj_run.exists(),
            self.proj_etc.exists(),
            self.proj_log.exists(),
            self.proj_tmp.exists(),
            self.proj_systemd.exists(),
        ]
        return all(all_run_dirs)

    def create(self):
        os.makedirs(
            self.proj_systemd,
            exist_ok=True
        )
        os.makedirs(
            self.proj_log,
            exist_ok=True
        )
        os.makedirs(
            self.proj_tmp,
            exist_ok=True
        )

    def filepath(self, filename=None):
        """
        filename given relative to project's run folder.
        E.g. rundir.filepath(etc/nginx.conf) => proj_dir/run/etc/nginx.conf
        """
        return self.proj_run / Path(filename)


def string_to_file(string, filepath, force=False):
    """
    filepath - is an instance of Pathlib.Path()
    """
    if filepath.exists() and not force:
        logger.error(
            f"file {filepath} already exists, to overwrite use -f"
        )
        return False

    with open(filepath, "w") as handle:
        handle.write(string)


class Command(BaseCommand):

    help = """Generates project's run/etc, run/log  folders
"""

    def get_context(self):
        context = {
            'proj_root': settings.PROJ_ROOT,
            'static_root': settings.STATIC_ROOT,
            'notice': NOTICE,
            'virt_env': sys.prefix,
            'media_root': settings.MEDIA_ROOT
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
            'etc/papermerge.env',
            'etc/gunicorn.conf.py',
            'etc/systemd/mg_nginx.service',
            'etc/systemd/papermerge.service',
            'etc/systemd/worker.service',
            'etc/systemd/papermerge.target',  # tracks deps
        ]:
            rendered = render_to_string(file, context)
            string_to_file(
                string=rendered,
                filepath=rundir.filepath(filename=file),
                force=force
            )
