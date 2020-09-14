import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from papermerge.core.models import Tag


from .utils import (
    create_root_user,
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

    def test_alltags_view(self):
        """
        GET /alltags/

        returns all tags of current user
        """
        Tag.objects.create(
            user=self.testcase_user,
            name="tag1"
        )
        Tag.objects.create(
            user=self.testcase_user,
            name="tag2"
        )

        alltags_url = reverse('core:alltags')

        ret = self.client.get(
            alltags_url,
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        tags = json.loads(ret.content)

        self.assertEquals(
            set([
                tag['name'] for tag in tags['tags']
            ]),
            set(["tag2", "tag1"])
        )
