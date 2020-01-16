import os
import logging
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Run specified SQL file.
"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--file-name',
            '-f',
            help="SQL file name"
        )

    def run_sql(
        self,
        sql_content=None
    ):
        with connection.cursor() as c:
            c.execute(sql_content)

    def handle(self, *args, **options):
        file_name = options.get(
            'file_name',
            False
        )
        core_path = apps.get_app_config('core').path

        full_sql_file_path = os.path.join(
            core_path,
            "pgsql",
            file_name
        )
        if not os.path.exists(full_sql_file_path):
            logger.debug(f"file {full_sql_file_path} not found")
            return

        sql_content = None
        with open(full_sql_file_path, 'rt') as f:
            sql_content = f.read()
            logger.debug(sql_content)

        if not sql_content:
            logger.debug(f"No SQL content available. Aborting.")
            return

        self.run_sql(
            sql_content=sql_content
        )
