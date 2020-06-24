import logging

from celery import Celery
from celery.apps.worker import Worker as CeleryWorker
from django.core.management.base import BaseCommand
from django.conf import settings
from papermerge.core.models import Document
from papermerge.core.importers.imap import import_attachment
from papermerge.core.importers.local import import_documents

logger = logging.getLogger(__name__)
celery_app = Celery('papermerge')


@celery_app.task
def txt2db():
    """
    Move OCRed text from txt files into database
    """
    logger.debug("Celery beat: txt2db")

    for doc in Document.objects.all():
        doc.update_text_field()


@celery_app.task
def import_from_email():
    """
    Import attachments from specified email account.
    """
    logger.debug("Celery beat: import_from_email")
    import_attachment()


@celery_app.task
def import_from_local_folder():
    """
    Import documents from defined local folder
    """
    logger.debug("Celery beat: import_from_local_folder")
    import_documents(settings.PAPERMERGE_IMPORTER_DIR)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls every 30 seconds txt2db, import_from_email,
    # and import_from_local_folder
    sender.add_periodic_task(
        30.0, txt2db.s(), name='txt2db'
    )
    sender.add_periodic_task(
        30.0, import_from_local_folder.s(), name='import_from_local_folder'
    )
    if not settings.PAPERMERGE_IMPORT_MAIL_USER:
        logger.info("PAPERMERGE_IMPORT_MAIL_USER not defined")
        return

    if not settings.PAPERMERGE_IMPORT_MAIL_HOST:
        logger.info("PAPERMERGE_IMPORT_MAIL_HOST not defined")
        return

    sender.add_periodic_task(
        30.0, import_from_email.s(), name='import_from_email'
    )


class Command(BaseCommand):

    help = """Async Celery Worker"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        celery_app.config_from_object(
            'django.conf:settings', namespace='CELERY'
        )

        # Load task modules from all registered Django app configs.
        celery_app.autodiscover_tasks()

        celery_worker = CeleryWorker(
            hostname="localhost",
            app=celery_app,
            beat=True
        )
        celery_worker.start()
