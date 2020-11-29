import os
import logging

from celery import Celery
from celery.apps.worker import Worker as CeleryWorker
from django.core.management.base import BaseCommand
from django.conf import settings
from papermerge.core.models import Document, BaseTreeNode
from papermerge.core.importers.imap import import_attachment
from papermerge.core.importers.local import import_documents

logger = logging.getLogger(__name__)
celery_app = Celery('papermerge')


@celery_app.task
def rebuild_the_tree():
    # https://github.com/django-mptt/django-mptt/issues/568
    BaseTreeNode.objects.rebuild()


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
    # if no email import defined, just skip the whole
    # thing.
    if not settings.PAPERMERGE_IMPORT_MAIL_USER:
        return

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
    # Calls every 64 seconds txt2db
    sender.add_periodic_task(
        64.0, txt2db.s(), name='txt2db'
    )
    # once every 5 minutes rebuild the whole tree
    sender.add_periodic_task(
        300, rebuild_the_tree.s(), name='rebuild_the_tree'
    )

    imp_dir_exists = None
    imp_dir = settings.PAPERMERGE_IMPORTER_DIR
    if settings.PAPERMERGE_IMPORTER_DIR:
        imp_dir_exists = os.path.exists(settings.PAPERMERGE_IMPORTER_DIR)

    if imp_dir and imp_dir_exists:
        sender.add_periodic_task(
            30.0, import_from_local_folder.s(), name='import_from_local_folder'
        )
    else:
        reason_msg = ""

        if not imp_dir:
            reason_msg += "1. IMPORDER_DIR not configured\n"
        if not imp_dir_exists:
            reason_msg += "2. importer dir does not exist\n"

        logger.warning(
            "Importer from local folder task not started."
            "Reason:\n" + reason_msg
        )

    mail_user = settings.PAPERMERGE_IMPORT_MAIL_USER
    mail_host = settings.PAPERMERGE_IMPORT_MAIL_HOST

    if mail_user and mail_host:
        sender.add_periodic_task(
            30.0, import_from_email.s(), name='import_from_email'
        )
    else:
        reason_msg = ""
        if not mail_user:
            reason_msg += "PAPERMERGE_IMPORT_MAIL_USER not defined\n"
        if not mail_host:
            reason_msg += "PAPERMERGE_IMPORT_MAIL_HOST not defined\n"

        logger.warning(
            "Importer from imap account not started."
            "Reason:\n" + reason_msg
        )


class Command(BaseCommand):

    help = """Async Celery Worker"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--pidfile',
            type=str,
            help='Optional file used to store the process pid.\n'
            'The program won’t start if this file already '
            'exists and the pid is still alive.'
        )

    def handle(self, *args, **options):
        celery_app.config_from_object(
            'django.conf:settings', namespace='CELERY'
        )
        # Load task modules from all registered Django app configs.
        celery_app.autodiscover_tasks()

        celery_worker = CeleryWorker(
            hostname="localhost",
            app=celery_app,
            beat=True,
            quiet=True,
            concurrency=1
        )

        # Set pidfile if it the corresponding argument has been provided
        if options['pidfile']:
            celery_worker.pidfile = options['pidfile']

        celery_worker.start()
