import logging

from django.conf import settings
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)


class MetadataPlugins:
    def __init__(self):
        self._plugins = []

        for plugin in settings.PAPERMERGE_METADATA_PLUGINS:
            self._plugins.append(
                import_string(plugin)
            )
