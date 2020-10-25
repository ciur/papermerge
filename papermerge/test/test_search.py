from django.test import TestCase
from django.contrib.auth import get_user_model
from papermerge.core.models import (
    Document, Page
)

from papermerge.search.backends import get_search_backend

User = get_user_model()


class TestPage(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test')

    def test_search_backend(self):
        backend = get_search_backend()
        backend.search("Great doc!", Document)

    def test_search_is_not_case_sensitive(self):
        """
        UT to double check that search by default is NOT case sensitive
        """
        backend = get_search_backend()

        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            page_count=5,
        )

        p = doc.pages.first()
        p.text = "search for TESTX text"
        p.save()

        result = backend.search("TESTX", Page)
        # it matches exact case
        self.assertEqual(
            result.count(), 1
        )

        result_case_insensitive_match = backend.search("testX", Page)
        # it matches lower and upper case mix
        self.assertEqual(
            result_case_insensitive_match.count(), 1
        )

        # no match for tst
        no_match = backend.search("tst", Page)
        self.assertEqual(
            no_match.count(), 0
        )
