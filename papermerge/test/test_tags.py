from pathlib import Path

from django.test import TestCase
from papermerge.core.models import (
    Document,
    Folder,
    ColoredTag
)
from papermerge.test.utils import create_root_user

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestDocument(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_basic_document_tagging(self):
        doc = Document.create_document(
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

        self.assertEquals(
            found_docs.count(),
            1
        )

        self.assertEquals(
            found_docs.first().title,
            "document_c"
        )
