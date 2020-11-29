import shutil
import os
import tempfile

from django.test import TestCase

from .utils import create_root_user
from papermerge.core.importers.local import import_documents
from papermerge.core.models import Document

BASE_DIR = os.path.dirname(__file__)


class TestLocalImporter(TestCase):
    def setUp(self):
        self.user = create_root_user()

    def test_pdf_local_importer(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        with tempfile.TemporaryDirectory() as tempdirname:
            shutil.copy(file_path, tempdirname)
            import_documents(tempdirname, skip_ocr=True)
        self.assertEqual(
            Document.objects.count(),
            1
        )

    def test_jpg_local_importer(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "page-1.jpg"
        )
        with tempfile.TemporaryDirectory() as tempdirname:
            shutil.copy(file_path, tempdirname)
            import_documents(tempdirname, skip_ocr=True)
        self.assertEqual(
            Document.objects.count(),
            1
        )

    def test_tar_local_importer(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "testdata.tar"
        )
        with tempfile.TemporaryDirectory() as tempdirname:
            shutil.copy(file_path, tempdirname)
            import_documents(tempdirname, skip_ocr=True)
        self.assertEqual(
            Document.objects.count(),
            0
        )

    def test_multiple_files_local_importer(self):
        file_path_tar = os.path.join(
            BASE_DIR,
            "data",
            "testdata.tar"
        )
        file_path_jpg = os.path.join(
            BASE_DIR,
            "data",
            "page-1.jpg"
        )
        file_path_pdf = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        with tempfile.TemporaryDirectory() as tempdirname:
            shutil.copy(file_path_pdf, tempdirname)
            shutil.copy(file_path_jpg, tempdirname)
            shutil.copy(file_path_tar, tempdirname)
            import_documents(tempdirname, skip_ocr=True)
        self.assertEqual(
            Document.objects.count(),
            2
        )
