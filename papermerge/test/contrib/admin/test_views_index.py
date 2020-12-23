from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponseRedirect

from papermerge.core.models import Document

from papermerge.test.utils import (
    create_root_user,
)


class AnonymouseUserIndexAccessView(TestCase):
    def setUp(self):
        # user exists, but not signed in
        self.testcase_user = create_root_user()
        self.client = Client()

    def test_index(self):
        ret = self.client.get(reverse('admin:index'))

        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )


class TestAdvancedSearchView(TestCase):
    """
    AV = advanced search
    """

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_basic_av_by_tag(self):
        """
        In advaced search user can search by tag(s)
        """
        doc1 = Document.objects.create_document(
            title="doc1",
            user=self.testcase_user,
            page_count=2,
            file_name="koko.pdf",
            size='1111',
            lang='ENG',
        )
        doc2 = Document.objects.create_document(
            title="doc2",
            user=self.testcase_user,
            page_count=2,
            file_name="kuku.pdf",
            size='1111',
            lang='ENG',
        )
        doc1.tags.add(
            "green",
            "blue",
            tag_kwargs={'user': self.testcase_user}
        )
        doc2.tags.add(
            "blue",
            tag_kwargs={'user': self.testcase_user}
        )

        ret = self.client.get(
            reverse('admin:search'), {'tag': 'green'}
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        self.assertEqual(
            len(ret.context['results_docs']),
            1
        )
        doc_ = ret.context['results_docs'][0]

        self.assertEqual(
            doc_.id,
            doc1.id
        )

    def test_basic_av_by_tags_op_all(self):
        """
        In advaced search user can search by tag(s)
        tags_op can be 'all' or 'any'.
        tags_op=all: find all documents which contain all tags
        """
        doc1 = Document.objects.create_document(
            title="doc1",
            user=self.testcase_user,
            page_count=2,
            file_name="koko.pdf",
            size='1111',
            lang='ENG',
        )
        doc2 = Document.objects.create_document(
            title="doc2",
            user=self.testcase_user,
            page_count=2,
            file_name="kuku.pdf",
            size='1111',
            lang='ENG',
        )
        doc3 = Document.objects.create_document(
            title="doc3",
            user=self.testcase_user,
            page_count=2,
            file_name="momo.pdf",
            size='1111',
            lang='ENG',
        )
        doc1.tags.add(
            "green",
            "blue",
            tag_kwargs={'user': self.testcase_user}
        )
        doc2.tags.add(
            "blue",
            tag_kwargs={'user': self.testcase_user}
        )
        doc3.tags.add(
            "green",
            "blue",
            "red",
            tag_kwargs={'user': self.testcase_user}
        )

        base_url = reverse('admin:search')
        args = "tag=green&tag=blue&tags_op=all"
        url = f"{base_url}?{args}"

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            200
        )
        self.assertEqual(
            len(ret.context['results_docs']),
            2
        )
        result_ids = set(
            [doc_.id for doc_ in ret.context['results_docs']]
        )
        self.assertEqual(
            result_ids,
            set([doc1.id, doc3.id])
        )

    def test_basic_av_by_tags_op_any(self):
        """
        In advaced search user can search by tag(s)
        tags_op can be 'all' or 'any'.
        tags_op=any: find all documents which contain any tags
        of the mentioned tags
        """
        doc1 = Document.objects.create_document(
            title="doc1",
            user=self.testcase_user,
            page_count=2,
            file_name="koko.pdf",
            size='1111',
            lang='ENG',
        )
        doc2 = Document.objects.create_document(
            title="doc2",
            user=self.testcase_user,
            page_count=2,
            file_name="kuku.pdf",
            size='1111',
            lang='ENG',
        )
        doc3 = Document.objects.create_document(
            title="doc3",
            user=self.testcase_user,
            page_count=2,
            file_name="momo.pdf",
            size='1111',
            lang='ENG',
        )
        doc1.tags.add(
            "red",
            tag_kwargs={'user': self.testcase_user}
        )
        doc2.tags.add(
            "green",
            tag_kwargs={'user': self.testcase_user}
        )
        doc3.tags.add(
            "blue",
            tag_kwargs={'user': self.testcase_user}
        )

        base_url = reverse('admin:search')
        args = "tag=red&tag=green&tags_op=any"
        url = f"{base_url}?{args}"

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            200
        )
        self.assertEqual(
            len(ret.context['results_docs']),
            2
        )
        result_ids = set(
            [doc_.id for doc_ in ret.context['results_docs']]
        )
        self.assertEqual(
            result_ids,
            set([doc1.id, doc2.id])
        )
