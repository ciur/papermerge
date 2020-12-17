import os
import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from papermerge.core.models import (
    Document,
    Folder,
    Access
)
from papermerge.core.auth import create_access
from papermerge.core.views.nodes import PER_PAGE


from .utils import (
    create_root_user,
    create_margaret_user,
    create_some_doc
)


BASE_DIR = os.path.dirname(__file__)


class TestBrowseView(TestCase):
    """
    Tests for json browse view
    """

    def setUp(self):

        self.root_user = create_root_user()
        self.margaret_user = create_margaret_user()
        self.client = Client()

    def test_browse_basic(self):

        Folder.objects.create(
            title="F1",
            user=self.root_user
        )

        Folder.objects.create(
            title="F2",
            user=self.root_user
        )

        self.client.login(testcase_user=self.root_user)

        ret = self.client.get(
            reverse('core:browse'),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        json_response = json.loads(ret.content)
        self.assertEqual(
            len(json_response['nodes']),
            2
        )

    def test_browse_with_pagination(self):
        """
        Will return only nodes of the first page + additional
        pagination info
        """
        for x in range(1, PER_PAGE + 2):
            Folder.objects.create(
                title=f"F_{x}",
                user=self.root_user
            )

        self.client.login(testcase_user=self.root_user)
        ret = self.client.get(
            reverse('core:browse'),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(
            ret.status_code,
            200
        )
        json_response = json.loads(ret.content)
        self.assertEqual(
            len(json_response['nodes']),
            PER_PAGE
        )
        self.assertEqual(
            json_response['pagination']['num_pages'],
            2
        )
        self.assertTrue(
            json_response['pagination']['page']['has_next'],
        )
        self.assertFalse(
            json_response['pagination']['page']['has_previous'],
        )

    def test_browse_with_parent(self):
        """
        Will return only the child nodes of specified parent
        """
        parent = Folder.objects.create(
            title="Parent",
            user=self.root_user
        )
        Folder.objects.create(
            title="Child1",
            user=self.root_user,
            parent=parent
        )
        Folder.objects.create(
            title="Child2",
            user=self.root_user,
            parent=parent
        )
        Folder.objects.create(
            title="Child3",
            user=self.root_user,
            parent=parent
        )

        self.client.login(testcase_user=self.root_user)
        ret = self.client.get(
            reverse('core:browse', args=(parent.id, )),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(
            ret.status_code,
            200
        )
        json_response = json.loads(ret.content)
        # will return children Child1, Child2, Child3
        self.assertEqual(
            len(json_response['nodes']),
            3
        )
        returned_node_titles_set = set([
            node['title'] for node in json_response['nodes']
        ])
        self.assertEqual(
            returned_node_titles_set,
            set(['Child1', 'Child2', 'Child3'])
        )

    def test_read_access_only(self):
        """
        User can access documents and folders only for which he/she
        has read access
        """
        Folder.objects.create(
            title="Root's Folder",
            user=self.root_user,
        )
        shared1 = Folder.objects.create(
            title="Shared 1",
            user=self.root_user,
        )
        shared2 = Folder.objects.create(
            title="Shared 2",
            user=self.root_user,
        )
        Folder.objects.create(
            title="Margaret's Folder",
            user=self.margaret_user,
        )
        create_access(
            node=shared1,
            model_type=Access.MODEL_USER,
            name=self.margaret_user,
            access_type=Access.ALLOW,
            access_inherited=False,
            permissions={
                Access.PERM_READ: True
            }  # allow read access to elizabet
        )
        create_access(
            node=shared2,
            model_type=Access.MODEL_USER,
            name=self.margaret_user,
            access_type=Access.ALLOW,
            access_inherited=False,
            permissions={
                Access.PERM_READ: True
            }  # allow read access to elizabet
        )
        self.client.login(testcase_user=self.margaret_user)
        # margaret will see 3 folders:
        # shared1 (which root user shared with her)
        # shared2 (which root shared with her)
        # and her own.
        ret = self.client.get(
            reverse('core:browse'),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEqual(
            ret.status_code,
            200
        )
        json_response = json.loads(ret.content)
        # will return children Child1, Child2, Child3
        self.assertEqual(
            len(json_response['nodes']),
            3
        )
        returned_node_titles_set = set([
            node['title'] for node in json_response['nodes']
        ])
        self.assertEqual(
            returned_node_titles_set,
            set(['Shared 1', 'Shared 2', "Margaret's Folder"])
        )


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


class TestNodesAnonymousUser(TestCase):

    def setUp(self):
        self.client = Client()

    def test_breadcrumb_view(self):

        ret = self.client.get(
            reverse('core:breadcrumb')
        )
        self.assertEqual(
            ret.status_code,
            302
        )
