import logging
from django.conf import settings


class DocumentImporter:

    def __init__(self, directory=settings.PAPERMERGE_IMPORTER_DIR):

        self.logger = logging.getLogger(__name__)
        # importer dir
        self.directory = directory

        if not self.directory:
            raise Exception("The PAPERMERGE_IMPORTER_DIR is not set.")
