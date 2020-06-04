import json

from django.test import Client, TestCase
from django.urls import reverse
from papermerge.core.models import Access, Folder
from papermerge.test.utils import create_margaret_user, create_uploader_user

READ = Access.PERM_READ
WRITE = Access.PERM_WRITE
DELETE = Access.PERM_DELETE
CHANGE_PERM = Access.PERM_CHANGE_PERM
TAKE_OWNERSHIP = Access.PERM_TAKE_OWNERSHIP

FULL_ACCESS = [
    Access.PERM_READ,
    Access.PERM_WRITE,
    Access.PERM_DELETE,
    Access.PERM_CHANGE_PERM,
    Access.PERM_TAKE_OWNERSHIP,
]


def get_dict_delete_access(
    username="margaret",
):
    post_data = {}
    access_entry = {
        "model": "user",
        "name": username,
        "access_type": "allow",
        "permissions": {}
    }
    post_data['delete'] = []
    post_data['delete'].append(access_entry)

    return post_data


def get_dict_add_access(
    username="margaret",
    read_perm=False,
    write_perm=False,
    delete_perm=False,
    change_perm=False,
    take_ownership=False
):
    post_data = {}
    access_entry = {
        "model": "user",
        "name": username,
        "access_type": "allow",
        "permissions": {
            "read": read_perm,
            "write": write_perm,
            "delete": delete_perm,
            "change_perm": change_perm,
            "take_ownership": take_ownership
        }
    }
    post_data['add'] = []
    post_data['add'].append(access_entry)

    return post_data


class TestAccessView(TestCase):

    def setUp(self):

        self.uploader_user = create_uploader_user()
        self.margaret_user = create_margaret_user()
        self.client = Client()

    def test_create_access(self):
        """
        Create access permissions for an existing folder.
        """
        new_folder = Folder.objects.create(
            title="test",
            user=self.uploader_user
        )
        # now margaret does not has read access
        self.assertFalse(
            self.margaret_user.has_perm(READ, new_folder)
        )
        post_data = {}
        access_entry = {
            "model": "user",
            "name": "margaret",  # username of self.margaret_user
            "access_type": "allow",
            "permissions": {
                "read": True
            }
        }
        post_data['add'] = []
        post_data['add'].append(access_entry)

        self.client.login(testcase_user=self.uploader_user)
        resp = self.client.post(
            reverse('core:access', args=(new_folder.id, )),
            post_data,
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        # and now margaret has read access
        self.assertTrue(
            self.margaret_user.has_perm(READ, new_folder)
        )

    def test_post_and_get_access(self):
        """
        1. Grant uploader user read, write & delete permissions.
        2. Check access:

                a. via HTTP GET
                b. via models

            that uploader has indeed - read, write and delete
            permissions.

        WBUG (was a bug): I created uploader, gave him
        read, write & delete permisions and... oopla, UI
        afterwards says that uploader has full permissions!
        """
        folder = Folder.objects.create(
            title="folderX",
            user=self.margaret_user
        )
        post_data = get_dict_add_access(
            username="uploader",
            read_perm=True,
            write_perm=True,
            delete_perm=True
        )

        self.client.login(testcase_user=self.margaret_user)

        resp = self.client.post(
            reverse('core:access', args=(folder.id, )),
            post_data,
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        self.assertTrue(
            self.uploader_user.has_perm(READ, folder)
        )
        self.assertTrue(
            self.uploader_user.has_perm(WRITE, folder)
        )
        self.assertTrue(
            self.uploader_user.has_perm(DELETE, folder)
        )
        self.assertFalse(
            self.uploader_user.has_perm(TAKE_OWNERSHIP, folder)
        )
        self.assertFalse(
            self.uploader_user.has_perm(CHANGE_PERM, folder)
        )
        # and now check that view will return same sort
        # of data
        resp = self.client.get(
            reverse('core:access', args=(folder.id, )),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        json_data = json.loads(resp.content)
        uploader_json = {}
        for user_json in json_data:
            if user_json['name'] == 'uploader':
                uploader_json = user_json

        self.assertTrue(
            uploader_json['permissions']['read']
        )
        self.assertTrue(
            uploader_json['permissions']['write']
        )
        self.assertTrue(
            uploader_json['permissions']['delete']
        )
        self.assertFalse(
            uploader_json['permissions']['take_ownership']
        )
        self.assertFalse(
            uploader_json['permissions']['change_perm']
        )

    def test_only_one_access_is_created(self):
        """
            Only one access item is created.

            There was a bug, that two access instances
            were created - one inherited and another not inherited -
            though only one HTTP POST /access/folder_id was issues
            and only of one (margaret user)
        """
        folder = Folder.objects.create(
            title="folder",
            user=self.uploader_user
        )
        post_data = get_dict_add_access(
            username="margaret",
            read_perm=True
        )

        self.client.login(testcase_user=self.uploader_user)
        resp = self.client.post(
            reverse('core:access', args=(folder.id, )),
            post_data,
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        # check that there is only one Access Entry with user margaret
        self.assertEqual(
            1,
            Access.objects.filter(
                node=folder,
                user=self.margaret_user
            ).count()
        )

    def test_add_and_remove(self):
        """
        1. Create one folder (uploader)
        2. Grant access to margaret as well
        3. Revoke margaret access
        """
        folder = Folder.objects.create(
            title="folder",
            user=self.uploader_user
        )
        post_data = get_dict_add_access(
            username="margaret",
            read_perm=True
        )

        self.client.login(testcase_user=self.uploader_user)
        resp = self.client.post(
            reverse('core:access', args=(folder.id, )),
            post_data,
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        self.assertTrue(
            self.margaret_user.has_perm(READ, folder)
        )
        self.assertTrue(
            self.uploader_user.has_perm(READ, folder)
        )
        post_data = get_dict_delete_access(
            username="margaret",
        )

        resp = self.client.post(
            reverse('core:access', args=(folder.id, )),
            post_data,
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        self.assertFalse(
            self.margaret_user.has_perm(READ, folder)
        )
        self.assertTrue(
            self.uploader_user.has_perm(READ, folder)
        )

    def test_access_is_created_recursively_via_view(self):
        """
        1. uploader creates:
            F1 -> L1a -> L2a -> L3a
            F1 -> L1b -> L2b

        2. Via View uploader user gives read access to margaret on F1
            HTTP POST /access/<folder_F1_id> ...

        3. Margaret will have read access on L1a, L1b, L2a, L2b,
            L3a as well (because of recursive inheritance)
        """
        F1 = Folder.objects.create(
            title="F1",
            user=self.uploader_user
        )
        L1a = Folder.objects.create(
            title="L1a",
            user=self.uploader_user,
            parent=F1
        )
        L2a = Folder.objects.create(
            title="L2a",
            user=self.uploader_user,
            parent=L1a
        )
        L3a = Folder.objects.create(
            title="L3a",
            user=self.uploader_user,
            parent=L2a
        )
        L1b = Folder.objects.create(
            title="L1b",
            user=self.uploader_user,
            parent=F1
        )
        L2b = Folder.objects.create(
            title="L2b",
            user=self.uploader_user,
            parent=L1b
        )
        post_data = {}
        access_entry = {
            "model": "user",
            "name": "margaret",  # username of self.margaret_user
            "access_type": "allow",
            "permissions": {
                "read": True
            }
        }
        post_data['add'] = []
        post_data['add'].append(access_entry)

        logged_in = self.client.login(
            testcase_user=self.uploader_user
        )
        self.assertTrue(
            logged_in,
            f"Auth failed for {self.uploader_user}"
        )
        resp = self.client.post(
            reverse('core:access', args=(F1.id, )),
            post_data,
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        for folder in [F1, L1a, L1b, L2a, L3a, L2b]:
            self.assertTrue(
                self.margaret_user.has_perm(READ, folder),
                f"Failed for folder {folder.title}"
            )
