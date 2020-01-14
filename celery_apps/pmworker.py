# Used in local dev env
import logging
import logging.config
from pmworker import setup_logging
from celery import Celery

app = Celery()
app.config_from_envvar('CELERY_CONFIG_MODULE')
logger = logging.getLogger(__name__)


setup_logging()
logger.debug(
    "Setup logging for pmworker complete."
)
