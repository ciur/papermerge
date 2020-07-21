import logging
import datetime
import os

from django.core.management import BaseCommand

from papermerge.core.backup_restore import backup_documents
from papermerge.core.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        Backup all documents and their folder structure to an archive.
        Backup is per specific user.

        By default backups only what is most important - your document files.

        You can trigger a full backup with --full-backup option
        (not yet implemented).

        Full backup will include:

            * OCRed text of each document/page (so that there
                 is no need to trigger an OCR during resoration)
            * metadata of each document
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'location',
            nargs='?',
            type=str,
            help="A directory or a file name (tar archive)."
            " If provided file is missing - will create one."
        )
        # Papermerge is multi-user system. There may be different users
        # with diferent folder structure each. Perform backup on specified one.
        parser.add_argument(
            "-u",
            "--user",
            help="username of the user to perform backup for."
        )
        parser.add_argument(
            '--full-backup',
            action='store_true',
            help="triggers full backup. Not yet implemented."
        )

    def handle(self, *args, **options):

        date_string = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
        default_filename = f"backup_{date_string}.tar"

        full_backup = options.get('full_backup')
        username = options.get('user')
        location = options.get('location') or default_filename

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            logger.error(
                f"Username {username} not found."
            )
            return

        # consider the case when user provides directory location i.e.
        # ./manage.py backup /backup/papermerge/

        if os.path.isdir(location):
            # in case location is a non existing directory path e.g. "blah/"
            # os.path.isdir will return False
            backup_location = os.path.join(location, default_filename)
        else:
            backup_location = location

        try:
            with open(backup_location, 'wb') as backup_file:
                backup_documents(
                    backup_file=backup_file,
                    user=user,
                    full_backup=full_backup
                )
        except IsADirectoryError:
            logger.error(
                "Provided location is a directory which does not exist."
                "Please create it first and try again."
            )
