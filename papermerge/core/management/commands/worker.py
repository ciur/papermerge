import time
import logging
from django.core.management.base import BaseCommand
from celery.apps.worker import Worker
from celery import Celery

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = """Async Celery Worker"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        celery_app = Celery()

        worker = Worker(
            hostname="localhost",
            app=celery_app
        )
        worker.start()
