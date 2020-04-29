import logging
from django.conf import settings


class DocumentImporter:

    def __init__(self, directory=settings.PAPERMERGE_IMPORTER_DIR):

        self.logger = logging.getLogger(__name__)
        self.directory = directory
