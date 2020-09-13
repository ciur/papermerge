from django.test import TestCase
from django.test import Client
from django.urls import reverse

from django.contrib.auth.models import Group

from .utils import (
    create_root_user,
)


class TestSearchView(TestCase):

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_basic_group_list(self):
        ret = self.client.get(
            reverse('core:groups'),
        )
        self.assertEquals(
            ret.status_code,
            200
        )

    def test_basic_groups_delete(self):
        gr1 = Group.objects.create(name="test1")
        gr2 = Group.objects.create(name="test2")

        self.assertEqual(
            Group.objects.count(),
            2
        )

        ret = self.client.post(
            reverse('core:groups'),
            {
                'action': 'delete_selected',
                '_selected_action': [gr1.id, gr2.id]
            }
        )
        self.assertEquals(
            ret.status_code,
            200
        )
        self.assertEqual(
            Group.objects.count(),
            0
        )

    def test_basic_group(self):
        gr = Group.objects.create(name="test")

        ret = self.client.get(
            reverse('core:group_change', args=(gr.id,)),
        )
        self.assertEquals(
            ret.status_code,
            200
        )

    def test_basic_group_new(self):
        ret = self.client.get(
            reverse('core:group'),
        )
        self.assertEquals(
            ret.status_code,
            200
        )

