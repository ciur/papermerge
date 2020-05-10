import logging
from django.core.management.base import BaseCommand
from celery.apps.worker import Worker
from celery import Celery

logger = logging.getLogger(__name__)
celery_app = Celery('papermerge')


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
        )
        worker.start()

