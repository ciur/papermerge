from pathlib import Path

from django.test import TestCase
from papermerge.core.models import (
    Document,
    Folder,
    Tag
)
from papermerge.test.utils import create_root_user

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestDocument(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_basic_document_tagging(self):
        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            page_count=5,
        )
        doc.save()

        # associate "invoice" and "paid" tags
        # boths tags belong to self.user
        doc.tags.add(
            "invoice",
            "paid",
            tag_kwargs={"user": self.user}
        )

        # If you’re filtering on multiple tags, it’s very common to get
        # duplicate results,
        # because of the way relational databases work. Often
        # you’ll want to make use of the distinct() method on QuerySets.
        found_docs = Document.objects.filter(
            tags__name__in=["paid", "invoice"]
        ).distinct()

        self.assertEqual(
            found_docs.count(),
            1
        )

        self.assertEqual(
            found_docs.first().title,
            "document_c"
        )

    def test_restore_multiple_tags(self):
        """
        Given a list of dictionaries with tag
        attributes - add those tags to the document
            (eventually create core.models.Tag instances).

        Keep in mind that tag instances need to belong to same user as the
        document owner.

        This scenario is used in restore script (restore from backup).
        """
        tag_attributes = [
            {
                "bg_color": "#ff1f1f",
                "fg_color": "#ffffff",
                "name": "important",
                "description": "",
                "pinned": True
            },
            {
                "bg_color": "#c41fff",
                "fg_color": "#FFFFFF",
                "name": "receipts",
                "description": None,
                "pinned": False
            }
        ]
        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            page_count=5,
        )
        doc.save()

        for attrs in tag_attributes:
            attrs['user'] = self.user
            tag = Tag.objects.create(**attrs)
            doc.tags.add(tag)

        doc.refresh_from_db()

        self.assertEqual(
            set([tag.name for tag in doc.tags.all()]),
            {"receipts", "important"}
        )

    def test_basic_folder_tagging(self):
        folder = Folder.objects.create(
            title="Markus",
            user=self.user
        )
        folder.tags.add(
            "invoices",
            tag_kwargs={"user": self.user}
        )
        found_folders = Folder.objects.filter(
            tags__name__in=["invoices"]
        )

        self.assertEqual(
            found_folders.count(),
            1
        )

        self.assertEqual(
            found_folders.first().title,
            "Markus"
        )
