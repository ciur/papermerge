from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .utils import (
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
        self.assertEquals(
            ret.status_code,
            200
        )
