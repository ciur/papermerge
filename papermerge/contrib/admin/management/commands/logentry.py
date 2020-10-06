import logging
from django.core.management.base import BaseCommand

from papermerge.contrib.admin.models import LogEntry

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = """
    Display/delete logentry count per user.

    Example:

    1. Delete all (i.e. for all users) logentries older than 2 days:

    ./manage.py logentry --delete -n 2d

    2. Without any argument will display logentries per user (for all users):

    ./manage.py logentry
"""

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--user',
            help="""
            Either user id or username of the user to display/delete
            logentries for. If ommited applies to all users.
        """
        )
        parser.add_argument(
            '-d',
            '--delete',
            help="Delete logentries",
            action="store_true"
        )
        parser.add_argument(
            '-n',
            '--number',
            default='7d',
            help="""
            Delete log entries older than <number><d|h|m|days|hours|minutes>.
            """
        )

    def handle(self, *args, **options):
        delete = options.get('delete')

        if delete:
            del_count, del_dict = LogEntry.objects.all().delete()
            print(f"Deleted {del_count} LogEntries.")
        else:
            count = LogEntry.objects.count()
            print(f"Total LogEntries count = {count}")
