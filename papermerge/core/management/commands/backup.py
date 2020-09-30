import logging
import datetime
import os

from django.core.management import BaseCommand

from papermerge.core.backup_restore import backup_documents
from papermerge.core.models import User

logger = logging.getLogger(__name__)


def list_users_and_exit():
    print("id\tusername\temail")
    print("----------------------------------")
    for user in User.objects.all():
        print(f"{user.id}\t{user.username}\t{user.email}")

    return True


class Command(BaseCommand):
    help = """
        Backup all documents and their folder structure to an archive.
        If --user/-u is specified - will backup all documents of
        the specific user.

        If --user/u is NOT specified - will backup documents of all users.
        --include-user-password will include user's password digest into backup
        archive
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
            help="""
            username of the user to perform backup for. If not given
            will perform backup for all users.
            """
        )
        parser.add_argument(
            "-p",
            "--include-user-password",
            action="store_true",
            # by default do not include user password's digest
            default=False,
            help="""
            Include user's password field (digest of user's password) into
            backup archive.
            """
        )
        parser.add_argument(
            "-l",
            "--list-users",
            action='store_true',
            help="List exiting users and quit."
        )

    def handle(self, *args, **options):

        date_string = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
        default_filename = f"backup_{date_string}.tar"

        username = options.get('user')
        location = options.get('location') or default_filename
        include_user_password = options.get('include_user_password')

        if options.get('list_users'):
            list_users_and_exit()
            return

        user = None
        if username:
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
                    include_user_password=include_user_password
                )
        except IsADirectoryError:
            logger.error(
                "Provided location is a directory which does not exist."
                "Please create it first and try again."
            )
