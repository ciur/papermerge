import logging

from django.core.management import BaseCommand
from papermerge.core.backup_restore import (
    _can_restore,
    _is_valid_user,
    restore_documents
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
        Restore all Documents and their folder structure from an archive.
        If you don't pass a username with --user you will be asked for it.

        By default will trigger OCR for each imported document.
        Use --skip-ocr if you wish to OCR documents later.
    """

    def add_arguments(self, parser):

        parser.add_argument(
            '--user', type=str,
            help="user (username of) the restored documents should belong to",
            default=None
        )
        # 1. Very useful option
        # during tests/development/maintenance of this module
        # 2. In case archive is full backup (i.e. includes OCR text info)
        #  can be skipped (that is the point of full backup - not to perform
        # OCR operation again).
        parser.add_argument(
            's',
            '--skip-ocr',
            action='store_true',
            help="will skip ",
        )

        parser.add_argument('location', nargs='?', type=str)

    def handle(self, *args, **options):

        skip_ocr = options.get('skip_ocr')

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
                        "Archive can be handled."
                        "Please enter the user (username of) that should"
                        " own the restored documents."
                    )

                    if _is_valid_user(username):
                        restore_documents(
                            restore_file=restore_file,
                            username=username,
                            skip_ocr=skip_ocr
                        )
                    else:
                        logging.error("User %s was not valid", username)
                else:
                    logging.error(
                        "Archive cannot be restored because of"
                        " version mismatch."
                    )
