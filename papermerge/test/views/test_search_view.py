from django.test import TestCase
from django.test import Client
from django.urls import reverse

from papermerge.core.models import Folder

from papermerge.test.utils import (
    create_root_user,
)


class TestSearchView(TestCase):

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_search(self):
        ret = self.client.get(
            reverse('admin:search'),
            {'q': "ok"}
        )
        self.assertEqual(
            ret.status_code,
            200
        )

    def test_search_with_matching_folders(self):
        """
        Cover case when there is a folder match.
        """
        Folder.objects.create(
            user=self.testcase_user,
            title="ok"
        )
        # if there is a folder match
        # folders will be displayed.
        ret = self.client.get(
            reverse('admin:search'),
            {'q': "ok"}
        )
        self.assertEqual(
            ret.status_code,
            200
        )
