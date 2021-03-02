import os
import json
from datetime import timedelta

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http.response import (
    HttpResponseForbidden
)

from rest_framework.test import APIClient
from rest_framework import status
from knox.models import AuthToken

from papermerge.core.models import (
    Document,
    Folder
)


from papermerge.test.utils import (
    create_root_user,
    create_margaret_user
)

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
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

        doc = Document.objects.create_document(
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

        doc = Document.objects.create_document(
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
        doc = Document.objects.create_document(
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
        self.margaret_user = create_margaret_user()
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
        ret = None
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
        doc = Document.objects.first()
        self.assertEquals(
            doc.parent.title,
            Folder.INBOX_NAME
        )

    def test_basic_documents_view(self):
        # create a basic document and assert
        # that api/documents returns it
        Document.objects.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        ret = self.client.get(
            reverse('core:api_documents')
        )

        self.assertEqual(
            ret.status_code, 200
        )
        docs = json.loads(ret.content)
        self.assertEqual(
            len(docs),
            1
        )

    def test_documents_returns_only_docs_user_has_perms_for_1(self):
        """
        User can list via API only docs he/she has access READ_ACCESS
        """
        # create a basic document and assert
        # that api/documents returns it
        Document.objects.create_document(
            title="berlin.pdf",
            user=self.margaret_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        ret = self.client.get(
            reverse('core:api_documents')
        )

        self.assertEqual(
            ret.status_code, 200
        )
        docs = json.loads(ret.content)
        # There is only one document in the system, and
        # only margaret has access to it (as owner)
        self.assertEqual(
            len(docs),
            0
        )

    def test_documents_returns_only_docs_user_has_perms_for_2(self):
        """
        User can list via API only docs he/she has access READ_ACCESS
        """
        # create a basic document and assert
        # that api/documents returns it
        Document.objects.create_document(
            title="berlin.pdf",
            user=self.margaret_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        Document.objects.create_document(
            title="doc1.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        Document.objects.create_document(
            title="doc2.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )

        ret = self.client.get(
            reverse('core:api_documents')
        )

        self.assertEqual(
            ret.status_code, 200
        )
        docs = json.loads(ret.content)
        # There is only one document in the system, and
        # only margaret has access to it (as owner)
        self.assertEqual(
            len(docs),
            2  # returns a list contaiing doc1.pdf and doc2.pdf
        )
        returned_titles = list(
            map(
                lambda x: x['title'],
                docs
            )
        )
        self.assertEquals(
            set(["doc1.pdf", "doc2.pdf"]),
            set(returned_titles)
        )

    def test_returns_only_doc_user_has_perms_for_1(self):
        """
        User can view via API only document he/she has access READ_ACCESS
        """
        doc = Document.objects.create_document(
            title="berlin.pdf",
            user=self.margaret_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        ret = self.client.get(
            reverse('core:api_document', args=(doc.id,))
        )

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_returns_only_doc_user_has_perms_for_2(self):
        """
        User can view via API only document he/she has access READ_ACCESS
        """
        doc = Document.objects.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        ret = self.client.get(
            reverse('core:api_document', args=(doc.id,))
        )

        self.assertEqual(
            ret.status_code,
            200
        )

        doc = json.loads(ret.content)
        self.assertEqual(
            doc['title'],
            "berlin.pdf"
        )

    def test_delete_denied_if_no_perm_granted(self):
        # document owned by margaret
        doc = Document.objects.create_document(
            title="berlin.pdf",
            user=self.margaret_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        # access is denied for testcase_user
        ret = self.client.delete(
            reverse('core:api_document', args=(doc.id,))
        )

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

        self.assertEqual(
            Document.objects.count(),
            1
        )

    def test_edit_denied_if_no_perm_granted(self):
        # document owned by margaret
        doc = Document.objects.create_document(
            title="berlin.pdf",
            user=self.margaret_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        # access is denied for testcase_user
        ret = self.client.put(
            reverse('core:api_document', args=(doc.id,)),
            {'title': "OK"},
            format="json"
        )

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

        self.assertEqual(
            Document.objects.count(),
            1
        )

    def test_can_edit_own_doc(self):
        # document owned by margaret
        doc = Document.objects.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        # access is denied for testcase_user
        ret = self.client.put(
            reverse('core:api_document', args=(doc.id,)),
            {'title': "OK.pdf"},
            format="json"
        )

        self.assertEqual(
            ret.status_code,
            200
        )

        doc_after_edit = json.loads(ret.content)

        self.assertEqual(doc_after_edit['id'], doc.id)
        self.assertEqual(doc_after_edit['title'], "OK.pdf")


class TestRestApiValidToken_With_InvalidToken(TestCase):
    def setUp(self):

        self.testcase_user = create_root_user()
        self.token = "Invalid Token"
        self.client = APIClient(
            HTTP_AUTHORIZATION=f"Token {self.token}",
        )

    def test_basic_documents_view(self):
        # create a basic document and assert
        # that api/documents returns it
        Document.objects.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        ret = self.client.get(
            reverse('core:api_documents')
        )

        # because user's token is invalid
        self.assertEqual(
            ret.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
