import os

from django.test import TestCase
from mglib.step import Step

from papermerge.core.import_pipeline import (
    go_through_pipelines,
)
from papermerge.core.storage import default_storage
from .utils import create_root_user

BASE_DIR = os.path.dirname(__file__)


class TestOCR(TestCase):
    def setUp(self):
        self.user = create_root_user()

    def make_init_kwargs(self, payload, processor):
        return {'payload': payload, 'processor': processor}

    def make_apply_kwargs(self, apply_async=False):
        return {'skip_ocr': False, 'apply_async': apply_async}

    def test_default_pipeline_jpg_ocr_async(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "page-1.jpg"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        init_kwargs = self.make_init_kwargs(
            payload=payload, processor='TEST')
        apply_kwargs = self.make_apply_kwargs(apply_async=True)
        doc = go_through_pipelines(init_kwargs, apply_kwargs)
        self.assertIsNotNone(doc)
        page_path = doc.get_page_path(
            page_num=1,
            step=Step(0),
        )
        img_abs_path = default_storage.abspath(
            page_path.img_url()
        )
        self.assertTrue(os.path.exists(img_abs_path))

    def test_default_pipeline_jpg_ocr_noasync(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "page-1.jpg"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        init_kwargs = self.make_init_kwargs(
            payload=payload, processor='TEST')
        apply_kwargs = self.make_apply_kwargs()
        doc = go_through_pipelines(init_kwargs, apply_kwargs)
        self.assertIsNotNone(doc)
        page_path = doc.get_page_path(
            page_num=1,
            step=Step(0),
        )
        img_abs_path = default_storage.abspath(
            page_path.img_url()
        )
        self.assertTrue(os.path.exists(img_abs_path))

    def test_default_pipeline_pdf_ocr_async(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        init_kwargs = self.make_init_kwargs(
            payload=payload, processor='TEST')
        apply_kwargs = self.make_apply_kwargs(apply_async=True)
        doc = go_through_pipelines(init_kwargs, apply_kwargs)
        self.assertIsNotNone(doc)
        page_path = doc.page_paths[1]
        hocr_abs_path = default_storage.abspath(page_path.hocr_url())
        self.assertTrue(os.path.exists(hocr_abs_path))

    def test_default_pipeline_pdf_ocr_noasync(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        init_kwargs = self.make_init_kwargs(
            payload=payload, processor='TEST')
        apply_kwargs = self.make_apply_kwargs()
        doc = go_through_pipelines(init_kwargs, apply_kwargs)
        self.assertIsNotNone(doc)
        page_path = doc.page_paths[1]
        hocr_abs_path = default_storage.abspath(page_path.hocr_url())
        self.assertTrue(os.path.exists(hocr_abs_path))
