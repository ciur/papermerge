import json

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http.response import (
    HttpResponseForbidden
)

from papermerge.core.models import Document


from .utils import (
    create_root_user,
    create_margaret_user
)


class TestApiView(TestCase):
    """
    Tests for core.views.api views
    """

    def setUp(self):

        self.testcase_user = create_root_user()
        self.margaret_user = create_margaret_user()
        self.client = Client()

    def test_pages_view(self):

        doc = Document.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3,
        )

        # margaret does not have access to the document
        self.client.login(testcase_user=self.margaret_user)

        post_data = [
            {'page_num': 2, 'page_order': 1},
            {'page_num': 1, 'page_order': 2},
            {'page_num': 3, 'page_order': 3}
        ]

        ret = self.client.post(
            reverse('core:api_pages', args=(doc.id, )),
            json.dumps(post_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEquals(
            ret.status_code,
            HttpResponseForbidden.status_code
        )
