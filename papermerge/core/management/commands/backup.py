import logging
import datetime
import os

from django.core.management import BaseCommand
from papermerge.core.backup_restore import backup_documents

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        Backup all documents and their folder structure to a archive.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'location',
            nargs='?',
            type=str,
            help="A directory or a file name (tar archive)."
            " If provided file is missing - will create one."
        )

    def handle(self, *args, **options):

        date_string = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
        default_filename = f"backup_{date_string}.tar"

        location = options.get('location') or default_filename

        # consider the case when user provides directory location i.e.
        # ./manage.py backup /backup/papermerge/

        if os.path.isdir(location):
            backup_location = os.path.join(location, default_filename)
        else:
            backup_location = location

        try:
            with open(backup_location, 'wb') as backup_file:
                backup_documents(backup_file)
        except IsADirectoryError:
            logger.error(
                "Provided location is a directory which does not exist."
                "Please create it first and try again."
            )
