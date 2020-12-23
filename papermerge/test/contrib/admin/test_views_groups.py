from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden

from django.contrib.auth.models import Group

from papermerge.test.utils import (
    create_root_user,
    create_margaret_user,
    create_user
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
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )


class TestGroupView(TestCase):

    def setUp(self):

        self.testcase_user = create_root_user()
        self.margaret_user = create_margaret_user()
        self.client = Client()

    def test_basic_group_list(self):
        self.client.login(testcase_user=self.testcase_user)

        Group.objects.create(name="test1")
        Group.objects.create(name="test2")

        ret = self.client.get(
            reverse('admin:groups'),
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        self.assertEqual(
            ret.context['object_list'].count(),
            2
        )

    def test_basic_groups_delete(self):
        self.client.login(testcase_user=self.testcase_user)

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
        self.assertEqual(
            ret.status_code,
            302
        )
        self.assertEqual(
            Group.objects.count(),
            0
        )

    def test_basic_group(self):
        self.client.login(testcase_user=self.testcase_user)

        gr = Group.objects.create(name="test")

        ret = self.client.get(
            reverse('admin:group-update', args=(gr.pk,)),
        )
        self.assertEqual(
            ret.status_code,
            200
        )

    def test_basic_group_new(self):
        self.client.login(testcase_user=self.testcase_user)

        ret = self.client.get(
            reverse('admin:group-add'),
        )
        self.assertEqual(
            ret.status_code,
            200
        )

    def test_create_new_group_via_post(self):
        """
        Asserts correct functionality of new group creation.
        """
        self.client.login(testcase_user=self.testcase_user)

        self.client.post(
            reverse('admin:group-add'),
            {'name': "new_group"}
        )

        self.assertEqual(
            Group.objects.count(),
            1
        )

    def test_change_group(self):
        """
        When updating a group, should not create a new
        entry, but update existing one!
        """
        self.client.login(testcase_user=self.testcase_user)

        gr = Group.objects.create(name="XXX")
        self.assertEqual(
            Group.objects.count(),
            1
        )

        self.client.post(
            reverse('admin:group-update', args=(gr.pk,)),
            {
                'name': "XXX2"
            }
        )
        self.assertEqual(
            Group.objects.count(),
            1
        )
        gr.refresh_from_db()
        self.assertEqual(
            gr.name,
            "XXX2"
        )

    def test_group_list_denied_for_margaret(self):
        """
        Margaret is a non-superuser (non-root) without any
        additional permissions assigned -> she will be denied
        access to list groups.
        """
        self.client.login(
            testcase_user=self.margaret_user
        )
        ret = self.client.get(
            reverse('admin:groups'),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_group_new_denied_for_margaret(self):
        """
        Margaret is a non-superuser (non-root) without any
        additional permissions assigned -> she won't be allowed
        adding a new group.
        """
        self.client.login(
            testcase_user=self.margaret_user
        )
        ret = self.client.get(
            reverse('admin:group-add'),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_group_change_denied_for_margaret(self):
        """
        Margaret is a non-superuser (non-root) without any
        additional permissions assigned -> she won't be allowed
        to perform changes on the group model.
        """
        gr = Group.objects.create(name="XXX")
        self.client.login(
            testcase_user=self.margaret_user
        )
        ret = self.client.post(
            reverse('admin:group-update', args=(gr.pk,)),
            {
                'name': "XXX2"
            }
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )
        gr.refresh_from_db()
        self.assertEqual(
            gr.name,
            "XXX"
        )

    def test_group_list_granted_given_correct_perm(self):
        """
        In order to get access to group list ``auth.view_group``
        permission is required.
        """
        user = create_user(
            username="non_priv",
            perms=['auth.view_group']
        )
        negative_case_user = create_user(
            username="other_perm_user",
            perms=['core.view_user']
        )
        Group.objects.create(name="XXX")

        self.client.login(
            testcase_user=user
        )
        ret = self.client.get(reverse('admin:groups'))

        self.assertEqual(
            ret.status_code,
            200
        )
        self.client.logout()
        # check negative case
        self.client.login(
            testcase_user=negative_case_user
        )
        ret = self.client.get(reverse('admin:groups'))

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_group_add_granted_given_correct_perm(self):
        """
        In order to add a group ``auth.add_group``
        permission is required.
        """
        user = create_user(
            username="non_priv",
            perms=['auth.add_group']
        )
        negative_case_user = create_user(
            username="other_perm_user",
            perms=['core.view_user']
        )
        Group.objects.create(name="XXX")

        self.client.login(
            testcase_user=user
        )
        ret = self.client.get(reverse('admin:group-add'))

        self.assertEqual(
            ret.status_code,
            200
        )
        # check negative case
        self.client.logout()
        self.client.login(
            testcase_user=negative_case_user
        )
        ret = self.client.get(reverse('admin:group-add'))

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )

    def test_group_change_granted_given_correct_perm(self):
        """
        In order to change a group ``auth.change_group``
        permission is required.
        """
        user = create_user(
            username="non_priv",
            perms=['auth.change_group']
        )
        negative_case_user = create_user(
            username="other_perm_user",
            perms=['core.view_user']
        )
        gr = Group.objects.create(name="XXX")

        self.client.login(
            testcase_user=user
        )
        ret = self.client.get(
            reverse('admin:group-update', args=(gr.id, ))
        )

        self.assertEqual(
            ret.status_code,
            200
        )
        # check negative case
        self.client.logout()
        self.client.login(
            testcase_user=negative_case_user
        )
        ret = self.client.get(
            reverse('admin:group-update', args=(gr.id, ))
        )

        self.assertEqual(
            ret.status_code,
            HttpResponseForbidden.status_code
        )
