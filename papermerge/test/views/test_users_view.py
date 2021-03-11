from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponseForbidden

from papermerge.test.utils import (
    create_root_user,
    create_margaret_user
)


class TestUsersView(TestCase):
    def setUp(self):

        self.root_user = create_root_user()
        self.margaret_user = create_margaret_user()
        self.client = Client()

    def test_basic_superuser(self):
        """
        Superuser can see listed all users
        """
        self.client.login(
            testcase_user=self.root_user
        )
        url = reverse('admin:users')

        ret = self.client.get(url)
        self.assertEqual(
            ret.status_code,
            200
        )

        self.assertEqual(
            ret.context['object_list'].count(),
            2
        )

    def test_basic_margaret(self):
        """
        For margaret listing users is not allowed
        (only superusers can list other users in the system)
        """
        self.client.login(
            testcase_user=self.margaret_user
        )
        url = reverse('admin:users')

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_margaret_cannot_add_user(self):
        self.client.login(
            testcase_user=self.margaret_user
        )
        url = reverse('admin:user-add')

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_margaret_cannot_change_user(self):
        self.client.login(
            testcase_user=self.margaret_user
        )
        url = reverse(
            'admin:user-update',
            args=(self.root_user.id,)
        )

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_margaret_cannot_change_user_password(self):
        """
        Margaret can change only her own password. To change
        other user's password view - access is denied.
        """
        self.client.login(
            testcase_user=self.margaret_user
        )
        url = reverse(
            'core:user_change_password',
            args=(self.root_user.id,)
        )

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )
