from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import Group

from papermerge.test.utils import (
    create_root_user,
)


class TestGroupViewUserNotAuth(TestCase):
    """
    Basic test to make sure that unauthorized users do not
    have access to group list
    """

    def test_basic_group_list(self):
        """
        No user is authenticated/signed in
        """
        Group.objects.create(name="test1")
        Group.objects.create(name="test2")

        ret = self.client.get(
            reverse('admin:groups'),
        )
        self.assertEquals(
            ret.status_code,
            HttpResponseRedirect.status_code
        )


class TestGroupView(TestCase):

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_basic_group_list(self):
        Group.objects.create(name="test1")
        Group.objects.create(name="test2")

        ret = self.client.get(
            reverse('admin:groups'),
        )
        self.assertEquals(
            ret.status_code,
            200
        )
        self.assertEquals(
            ret.context['object_list'].count(),
            2
        )

    def test_basic_groups_delete(self):
        gr1 = Group.objects.create(name="test1")
        gr2 = Group.objects.create(name="test2")

        self.assertEqual(
            Group.objects.count(),
            2
        )

        ret = self.client.post(
            reverse('admin:groups'),
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
            reverse('admin:group_change', args=(gr.id,)),
        )
        self.assertEquals(
            ret.status_code,
            200
        )

    def test_basic_group_new(self):
        ret = self.client.get(
            reverse('admin:group'),
        )
        self.assertEquals(
            ret.status_code,
            200
        )

    def test_change_group(self):
        """
        When updating a group, should not create a new
        entry, but update existing one!
        """
        gr = Group.objects.create(name="XXX")
        self.assertEquals(
            Group.objects.count(),
            1
        )

        self.client.post(
            reverse('admin:group_change', args=(gr.id,)),
            {
                'name': "XXX2"
            }
        )
        self.assertEquals(
            Group.objects.count(),
            1
        )
        gr.refresh_from_db()
        self.assertEquals(
            gr.name,
            "XXX2"
        )
