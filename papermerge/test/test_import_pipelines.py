import random
import string
import os

from django.test import TestCase, override_settings

from .utils import create_root_user
from papermerge.core.import_pipeline import (
    go_through_pipelines,
    IMAP,
    LOCAL,
    WEB,
    DefaultPipeline
)

BASE_DIR = os.path.dirname(__file__)


PAPERMERGE_DEFAULT_PIPELINE = [
    'papermerge.core.import_pipeline.DefaultPipeline'
]
PAPERMERGE_SIMPLE_PIPELINE = [
    'papermerge.test.test_import_pipelines.PipelineOne',
    'papermerge.core.import_pipeline.DefaultPipeline',
]
PROCESSORS = [WEB, LOCAL, IMAP, 'TEST']
MAGIC_BYTES = [
    ('pdf', b'\x25\x50\x44\x46\x2d'),
    ('txt', b''),
    ('jpg', b'\xFF\xD8\xFF\xDB')
]


class TestSimplePipelineBytes(TestCase):
    def setUp(self):
        self.user = create_root_user()

    def make_init_kwargs(self, payload, processor):
        return {'payload': payload, 'processor': processor}

    def make_apply_kwargs(self, apply_async=False):
        return {'skip_ocr': True, 'apply_async': apply_async}

    @override_settings(PAPERMERGE_PIPELINES=PAPERMERGE_SIMPLE_PIPELINE)
    def test_simple_pipeline_pdf(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        for processor in PROCESSORS:
            init_kwargs = self.make_init_kwargs(
                payload=payload, processor=processor)
            apply_kwargs = self.make_apply_kwargs()
            doc = go_through_pipelines(init_kwargs, apply_kwargs)
            self.assertIsNotNone(doc)
            self.assertEqual(doc.name, 'test_change_name')

    @override_settings(PAPERMERGE_PIPELINES=PAPERMERGE_SIMPLE_PIPELINE)
    def test_simple_pipeline_txt(self):
        payload_data = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=100)).encode()
        payload = b''.join([MAGIC_BYTES[1][1], payload_data])
        for processor in PROCESSORS:
            init_kwargs = self.make_init_kwargs(
                payload=payload, processor=processor)
            apply_kwargs = self.make_apply_kwargs()
            doc = go_through_pipelines(init_kwargs, apply_kwargs)
            self.assertIsNone(doc)

    @override_settings(PAPERMERGE_PIPELINES=PAPERMERGE_SIMPLE_PIPELINE)
    def test_simple_pipeline_jpg(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "page-1.jpg"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        for processor in PROCESSORS:
            init_kwargs = self.make_init_kwargs(
                payload=payload, processor=processor)
            apply_kwargs = self.make_apply_kwargs()
            doc = go_through_pipelines(init_kwargs, apply_kwargs)
            self.assertIsNotNone(doc)
            self.assertEqual(doc.name, 'test_change_name')


class TestDefaultPipelineBytes(TestCase):
    def setUp(self):
        self.user = create_root_user()

    def make_init_kwargs(self, payload, processor):
        return {'payload': payload, 'processor': processor}

    def make_apply_kwargs(self, apply_async=False):
        return {'skip_ocr': True, 'apply_async': apply_async}

    @override_settings(PAPERMERGE_PIPELINES=PAPERMERGE_DEFAULT_PIPELINE)
    def test_default_pipeline_pdf(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        for processor in PROCESSORS:
            init_kwargs = self.make_init_kwargs(
                payload=payload, processor=processor)
            apply_kwargs = self.make_apply_kwargs()
            doc = go_through_pipelines(init_kwargs, apply_kwargs)
            self.assertIsNotNone(doc)

    @override_settings(PAPERMERGE_PIPELINES=PAPERMERGE_DEFAULT_PIPELINE)
    def test_default_pipeline_txt(self):
        payload_data = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=100)).encode()
        payload = b''.join([MAGIC_BYTES[1][1], payload_data])
        for processor in PROCESSORS:
            init_kwargs = self.make_init_kwargs(
                payload=payload, processor=processor)
            apply_kwargs = self.make_apply_kwargs()
            doc = go_through_pipelines(init_kwargs, apply_kwargs)
            self.assertIsNone(doc)

    @override_settings(PAPERMERGE_PIPELINES=PAPERMERGE_DEFAULT_PIPELINE)
    def test_default_pipeline_jpg(self):
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "page-1.jpg"
        )
        with open(file_path, 'rb') as f:
            payload = f.read()
        for processor in PROCESSORS:
            init_kwargs = self.make_init_kwargs(
                payload=payload, processor=processor)
            apply_kwargs = self.make_apply_kwargs()
            doc = go_through_pipelines(init_kwargs, apply_kwargs)
            self.assertIsNotNone(doc)


class PipelineOne(DefaultPipeline):
    def get_init_kwargs(self):
        return None

    def get_apply_kwargs(self):
        name = 'test_change_name'
        return {'name': name}

    def apply(self, **kwargs):
        pass
