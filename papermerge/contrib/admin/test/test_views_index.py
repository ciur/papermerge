from django.test import TestCase
from django.test import Client
from django.urls import reverse

from papermerge.core.models import Document

from papermerge.test.utils import (
    create_root_user,
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
        tags_op can be 'all' or 'any'.
        tags_op=all: find all documents which contain all tags
        tags_op=any: find all documents which contain at least one of tags
        """
        doc1 = Document.create_document(
            title="doc1",
            user=self.testcase_user,
            page_count=2,
            file_name="koko.pdf",
            size='1111',
            lang='ENG',
        )
        doc2 = Document.create_document(
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
            reverse('admin:search'),
            {
                'tag': 'green',
                'tags_op': 'all'
            }
        )
        self.assertEquals(
            ret.status_code,
            200
        )
        self.assertEquals(
            len(ret.context['results_docs']),
            1
        )
        doc_ = ret.context['results_docs'][0]
        self.assertEquals(doc_.id, doc1.id)
