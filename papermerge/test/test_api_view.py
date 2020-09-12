import os
import json
from datetime import timedelta

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http.response import (
    HttpResponseForbidden
)
from django.test.client import (
    RequestFactory,
    encode_multipart
)

from rest_framework.test import APIClient
from knox.models import AuthToken

from papermerge.core.models import Document
from papermerge.core.views.api import DocumentUploadView


from .utils import (
    create_root_user,
    create_margaret_user
)

BASE_DIR = os.path.dirname(__file__)


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

    def test_cut_view(self):

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

        post_data = [1, 2]

        ret = self.client.post(
            reverse('core:api_pages_cut', args=(doc.id, )),
            json.dumps(post_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEquals(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_paste_view_access_forbidden(self):
        """
        Access forbidden for margaret
        """
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

        post_data = [1, 2]

        ret = self.client.post(
            reverse('core:api_pages_paste', args=(doc.id, )),
            json.dumps(post_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEquals(
            ret.status_code,
            HttpResponseForbidden.status_code
        )


class TestRestApiWithValidToken(TestCase):
    """
    Tests for REST API assuming a valid
    token
    """

    def setUp(self):

        self.testcase_user = create_root_user()
        self.token = self._create_token(
            self.testcase_user
        )
        self.client = APIClient(
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

    def _create_token(self, user):
        instance, token = AuthToken.objects.create(
            user=user,
            expiry=timedelta(hours=32)
        )

        return token

    def test_basic_upload(self):
        """
        Upload a document given a valid token
        """
        # notice, there was no login
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )

        with open(file_path, "rb") as fp:
            data = {
                'file': fp
            }
            ret = self.client.put(
                reverse(
                    'core:api_document_upload', args=(
                        'berlin.pdf',
                    )
                ),
                data,
                format='multipart'
            )
            self.assertEqual(
                ret.status_code, 200
            )

        self.assertEquals(
            Document.objects.count(),
            1
        )
