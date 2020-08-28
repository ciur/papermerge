import os
import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from papermerge.core.models import Document


from .utils import (
    create_root_user,
    create_some_doc
)


BASE_DIR = os.path.dirname(__file__)


class TestNodesView(TestCase):
    """
    Tests operations on the document via Ajax e.g.
    edit fields, delete document.
    """

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_delete_node(self):
        """
        DELETE /node/<node_id>
        """
        doc = create_some_doc(
            self.testcase_user,
            page_count=1
        )
        self.assertEqual(
            Document.objects.count(),
            1
        )

        nodes_url = reverse(
            'core:node', args=(doc.id,)
        )

        ret = self.client.delete(
            nodes_url,
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        self.assertEqual(
            Document.objects.count(),
            0
        )

    def test_delete_nodes(self):
        """
        POST /nodes/
        with post data a list of dictionaries which should
        contain at least doc ids
        """
        doc1 = create_some_doc(
            self.testcase_user,
            page_count=1
        )
        doc2 = create_some_doc(
            self.testcase_user,
            page_count=1
        )
        self.assertEqual(
            Document.objects.count(),
            2
        )

        nodes_url = reverse(
            'core:nodes'
        )

        nodes_data = [
            {'id': doc1.id},
            {'id': doc2.id}
        ]

        ret = self.client.post(
            nodes_url,
            json.dumps(nodes_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        self.assertEqual(
            Document.objects.count(),
            0
        )

