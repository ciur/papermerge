from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase
from papermerge.core.models import Document, Page

User = get_user_model()

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestPage(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin')

    def get_whatever_doc(self):
        return Document.create_document(
            title="kyuss.pdf",
            user=self.user,
            lang="ENG",
            file_name="kyuss.pdf",
            size=1222,
            page_count=3
        )

    def test_language_is_inherited(self):
        """
        Whatever document model has in doc.lang field
        will be inherited by the related page models.
        """
        doc = Document.create_document(
            title="kyuss.pdf",
            user=self.user,
            lang="ENG",
            file_name="kyuss.pdf",
            size=1222,
            page_count=3
        )

        doc.save()

        self.assertEqual(
            doc.page_set.count(),
            3
        )

        langs = [
            page.lang for page in doc.page_set.all()
        ]

        self.assertEqual(
            ['ENG', 'ENG', 'ENG'],
            langs
        )

    def test_recreate_page_models(self):
        doc = Document.create_document(
            title="kyuss.pdf",
            user=self.user,
            lang="ENG",
            file_name="kyuss.pdf",
            size=1222,
            page_count=3
        )

        doc.save()

        self.assertEqual(
            doc.page_set.count(),
            3
        )
        doc.page_set.all().delete()
        self.assertEqual(
            doc.page_set.count(),
            0
        )

    def test_page_matching_search(self):
        doc = self.get_whatever_doc()
        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        result = Page.objects.search("cool")

        self.assertEquals(
            result.count(),
            1
        )

    def test_page_not_matching_search(self):
        doc = self.get_whatever_doc()
        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        result = Page.objects.search("andromeda")

        self.assertEquals(
            result.count(),
            0
        )
