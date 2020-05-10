import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from celery.apps.worker import Worker
from celery import Celery
from papermerge.core.importers.imap import import_attachment as main_imp_atta
from papermerge.core.importers.local import import_documents as main_doc_imp

logger = logging.getLogger(__name__)
celery_app = Celery('papermerge')


@celery_app.task
def import_attachment():
    logger.info("import attachment")
    main_imp_atta()


@celery_app.task
def import_documents(directory):
    logger.info("importing documents")
    main_doc_imp(directory)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    directory = settings.PAPERMERGE_IMPORTER_DIR
    logger.info("Hello!")
    sender.add_periodic_task(
        10.0, import_attachment.s(), name='Import attachments'
    )
    sender.add_periodic_task(
        10.0, import_documents.s(directory), name="Import documents"
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

        worker = Worker(
            hostname="localhost",
            app=celery_app,
            beat=True
        )
        worker.start()

