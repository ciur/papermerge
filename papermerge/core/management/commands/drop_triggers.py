from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = """In version 1.2 there were triggers defined
Since version 1.4, triggers are not used anymore
"""

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "DROP TRIGGER IF EXISTS "
                "tsvector_update_core_page ON core_page"
            )
            cursor.execute(
                "DROP TRIGGER IF EXISTS "
                " tsvector_update_core_basetreenode ON core_page"
            )
