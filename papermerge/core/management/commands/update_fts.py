import logging
from django.core.management.base import BaseCommand
from django.db import connection

from papermerge.core.utils import get_sql_content

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Run specified SQL file.
"""

    def run_sql(
        self,
        sql_content=None
    ):
        with connection.cursor() as c:
            c.execute(sql_content)

    def handle(self, *args, **options):

        self.run_sql(
            sql_content=get_sql_content("03_update_lang_cols.sql")
        )
