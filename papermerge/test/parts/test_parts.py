from django.test import TestCase

from papermerge.core.models import Document
from papermerge.test.utils import create_root_user

from papermerge.test.parts.app_dr.models import Policy

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

    def test_create_a_simple_document(self):
        policy = Policy.objects.create(name="Default Policy")

        doc = Document.objects.create_document(
            file_name="test.pdf",
            title="Test #1",
            page_count=3,
            size="3",
            lang="DEU",
            user=self.user,
            parts={
                'policy': policy
            }
        )

        self.assertEqual(
            doc.title,
            "Test #1"
        )
        self.assertEqual(
            doc.parts.policy.name,
            "Default Policy"
        )

    def test_assign_policy_after_document_creation(self):

        doc = Document.objects.create_document(
            file_name="test.pdf",
            size="3",
            lang="DEU",
            user=self.user,
            title="Test #1",
            page_count=3,
        )

        self.assertEqual(
            doc.title,
            "Test #1"
        )
        policy = Policy.objects.create(
            name="Default Policy"
        )
        self.assertFalse(
            doc.parts.policy
        )

        doc.parts.policy = policy
        doc.save()
        doc.refresh_from_db()

        dox = Document.objects.get(id=doc.id)

        self.assertEqual(
            dox.parts.policy.name,
            "Default Policy"
        )
