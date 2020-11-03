from django.test import TestCase

from papermerge.core.models import Document
from papermerge.test.utils import create_root_user

class PartsTests(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_basic(self):
        doc = Document.objects.create_document(
            file_name="test.pdf",
            title="Test #1",
            page_count=3,
            size="3",
            lang="DEU",
            user=self.user,
            parts={
                "extra_special_id": "DOC_XYZ_1"
            }
        )

        self.assertTrue(doc)
        self.assertEqual(
            doc.parts.extra_special_id,
            "DOC_XYZ_1"
        )
