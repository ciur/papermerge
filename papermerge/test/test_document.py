import os
from pathlib import Path

from django.test import TestCase
from papermerge.test.utils import create_root_user

from papermerge.core.models import (
    Document,
    Folder
)

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestDocument(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_tree_path(self):
        """
        Create following structure:
            Folder A > Folder B > Document C
        and check ancestors of Document C
        """

        folder_a = Folder.objects.create(
            title="folder_a",
            user=self.user,
            parent_id=None
        )
        folder_a.save()

        folder_b = Folder.objects.create(
            title="folder_b",
            user=self.user,
            parent_id=folder_a.id
        )
        folder_b.save()

        doc = Document.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder_b.id,
            page_count=5,
        )
        doc.save()
        ancestors = [
            [node.title, node.id]
            for node in doc.get_ancestors(include_self=True)
        ]
        self.assertListEqual(
            ancestors,
            [
                ['folder_a', folder_a.id],
                ['folder_b', folder_b.id],
                ['document_c', doc.id]
            ]
        )
        self.assertEqual(
            doc.page_set.count(),
            5
        )

    def test_delete_document_with_parent(self):
        """
        Document D is child of folder F.
        Deleting document D, will result in... well...
        no more D around, but F still present.
        """
        folder = Folder.objects.create(
            user=self.user,
            title="F"
        )

        doc = Document.create_document(
            title="andromeda.pdf",
            user=self.user,
            lang="ENG",
            file_name="andromeda.pdf",
            size=1222,
            page_count=3
        )

        doc.parent = folder
        doc.save()
        folder.save()

        self.assertEqual(
            folder.get_children().count(),
            1
        )
        self.assertEqual(
            doc.page_set.count(),
            3
        )

        doc.delete()

        self.assertEqual(
            folder.get_children().count(),
            0
        )

        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(title="D")

    def test_import_file(self):
        src_file_path = os.path.join(
            BASE_DIR, "data", "andromeda.pdf"
        )

        ret = Document.import_file(
            filepath=src_file_path,
            start_ocr_async=False,
            upload=False
        )

        self.assertTrue(ret, "Storage Quota reached for the user.")

        self.assertEqual(
            Document.objects.filter(title="andromeda.pdf").count(),
            1,
            "Document andromeda.pdf was not created."
        )

    def test_import_file_with_title_arg(self):
        src_file_path = os.path.join(
            BASE_DIR, "data", "andromeda.pdf"
        )

        ret = Document.import_file(
            filepath=src_file_path,
            start_ocr_async=False,
            file_title="X1.pdf",
            upload=False
        )

        self.assertTrue(ret, "Storage Quota reached for the user.")

        self.assertEqual(
            Document.objects.filter(title="X1.pdf").count(),
            1,
            "Document X1.pdf was not created."
        )

    def test_import_file_with_username_arg(self):
        src_file_path = os.path.join(
            BASE_DIR, "data", "andromeda.pdf"
        )

        ret = Document.import_file(
            username="root",
            filepath=src_file_path,
            start_ocr_async=False,
            file_title="X1.pdf",
            upload=False
        )

        self.assertTrue(ret, "Storage Quota reached for the user.")

        self.assertEqual(
            Document.objects.filter(title="X1.pdf").count(),
            1,
            "Document X1.pdf was not created."
        )

    def test_update_text_field(self):
        """
        basic test for doc.update_text_field()
        """
        doc = Document.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=None,
            page_count=5,
        )
        doc.save()
        doc.update_text_field()
