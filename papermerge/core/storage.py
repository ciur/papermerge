import logging
from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


def get_storage_class(import_path=None):
    return import_string(
        import_path or settings.PAPERMERGE_DEFAULT_FILE_STORAGE
    )


storage_class = get_storage_class()


default_storage = storage_class(
    location=settings.MEDIA_ROOT
)
