import datetime

from django.core.management import BaseCommand
from papermerge.core.backup_restore import backup_documents


class Command(BaseCommand):
    help = """
        Backup all Documents and their folder structure to a archive.
         
    """

    def add_arguments(self, parser):
        parser.add_argument('location',nargs='?', type=str)

    def handle(self, *args, **options):
        if options.get('location') is None:
            date_string = datetime.datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
            backup_location = 'backup_%s.tar'%(date_string)
        else:
            backup_location = options.get('location')
        with open(backup_location, 'wb') as backup_file:
            backup_documents(backup_file)
