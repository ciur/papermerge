import logging

from django.core.management import BaseCommand
from papermerge.core.backup_restore import _can_restore, _is_valid_user, restore_documents

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        Restore all Documents and their folder structure from an archive.
        If you don't pass a user with --user you will be asked for it.
    """

    def add_arguments(self, parser):
        parser.add_argument('--user', type=str,
                            help="user the restored documents should belong to", default=None)
        parser.add_argument('location', nargs='?', type=str)

    def handle(self, *args, **options):
        if options.get('location') is None:
            logger.error("Please add the path to your backup.tar")
        else:
            with open(options.get('location'), 'rb') as restore_file:
                if _can_restore(restore_file):
                    if options.get('user') is None:
                        username = input("Username:")
                    else:
                        username = options.get('user')
                    logging.info(
                        "We can handle that archive. Please enter the user that should own the restored documents.")

                    if _is_valid_user(username):
                        restore_documents(restore_file, username)
                    else:
                        logging.error("User %s was not valid", username)
                else:
                    logging.error("Looks like we can't understand your archive. Please make sure it is valid!")
