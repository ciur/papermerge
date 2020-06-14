import logging

from django.conf import settings
from django.utils.module_loading import import_string
from mglib.step import Step

from .models import Document
from .storage import default_storage

logger = logging.getLogger(__name__)


class MetadataPlugins:

    def __init__(self):
        self._plugins = []

        for plugin in settings.PAPERMERGE_METADATA_PLUGINS:
            self._plugins.append(
                import_string(plugin)
            )

    def apply(self, hocr_path):
        for plugin in self._plugins:
            if plugin.identify(hocr_path):
                return plugin.extract(hocr_path)


def apply_metadata_plugins(document_id, page_num):

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        logger.error(f"Provided document_id={document_id}, does not exists")
        return

    page_path = document.get_page_path(
        page_num=page_num,
        step=Step(),
    )
    hocr_path = default_storage.abspath(page_path.hocr_url())
    metadata_plugins = MetadataPlugins()

    return metadata_plugins.apply(hocr_path)
