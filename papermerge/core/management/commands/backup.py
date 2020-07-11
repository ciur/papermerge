from django.core.management import BaseCommand
from papermerge.core.backup_restore import backup_documents

class Command(BaseCommand):
    help = """
        Backup all Documents and their folder structure to a archive.
        Backupfolder is defined by PAPERMERGE_BACKUP_DIR configuration setting.
    """

    def handle(self, *args, **options):
        backup_documents('backup.tar')


        pass
