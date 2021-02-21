import json

from django.test import Client, TestCase
from django.urls import reverse
from papermerge.core.models import (
    Access,
    Folder,
    Page
)
from papermerge.test.utils import (
    create_margaret_user,
    create_elizabet_user,
    create_uploader_user,
    create_root_user,
    create_some_doc
)
from papermerge.core.models.kvstore import MONEY


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
        json_data = json_data.get('access', [])
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


class TestMetadataAccessView(TestCase):
    """
    If user has readonly access to folder/document, then
    he/she cannot delete/change node's metadata
    """

    def setUp(self):
        self.root_user = create_root_user()
        self.margaret_user = create_margaret_user()
        self.elizabet_user = create_elizabet_user()

    def test_metadata_is_readonly(self):
        """
        superuser creates a folder - for_margaret - and
        gives margaret readonly access on that folder.
        for_margaret folder contains two documents doc_1 and doc_2.

        Expected (for all 3 nodes - a folder and 2 documents):
            * margaret can see/read metadata
            * margaret cannot delete/change metadata
        """
        for_margaret = Folder.objects.create(
            title="for_margaret",
            user=self.root_user
        )
        doc_1 = create_some_doc(
            user=self.root_user,
            parent_id=for_margaret.id
        )
        doc_2 = create_some_doc(
            user=self.root_user,
            parent_id=for_margaret.id
        )
        for_margaret.refresh_from_db()

        self.assertEqual(
            for_margaret.get_children().count(),
            2
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
            testcase_user=self.root_user
        )
        self.assertTrue(
            logged_in,
            f"Auth failed for {self.root_user}"
        )
        resp = self.client.post(
            reverse('core:access', args=(for_margaret.id, )),
            post_data,
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 200
        )
        self.client.logout()

        # Preparetion ready #
        # Now, let margaret change metadata on folder
        # for_margaret
        logged_in = self.client.login(
            testcase_user=self.margaret_user
        )
        self.assertTrue(
            logged_in,
            f"Auth failed for {self.margaret_user}"
        )
        resp = self.client.post(
            reverse('core:metadata', args=('node', for_margaret.id)),
            {},  # does not matter, must be unauthorized
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 403
        )
        # same for doc_1
        resp = self.client.post(
            reverse('core:metadata', args=('node', doc_1.id)),
            {},  # does not matter, must be unauthorized
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 403
        )
        # same for doc_2
        resp = self.client.post(
            reverse('core:metadata', args=('node', doc_2.id)),
            {},  # does not matter, must be unauthorized
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 403
        )

        page = Page.objects.filter(
            document=doc_1
        ).first()
        # similarely, margaret cannot change
        # metadata the page
        resp = self.client.post(
            reverse('core:metadata', args=('page', page.id)),
            {},  # does not matter, must be unauthorized
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(
            resp.status_code, 403
        )

    def test_metadata_cannot_be_accessed_by_other_users(self):
        """
        margaret cannot access elizabet documents' metadata
        """
        elizabet_doc = create_some_doc(
            user=self.elizabet_user,
            page_count=2
        )

        # elizabet's doc has metadata
        elizabet_doc.kv.update(
            [
                {
                    'key': 'price',
                    'kv_type': MONEY,
                    'kv_format': 'dd,cc',
                }
            ]
        )
        elizabet_doc.assign_kv_values({'price': '10,00'})
        page_1 = Page.objects.get(document=elizabet_doc, number=1)
        page_2 = Page.objects.get(document=elizabet_doc, number=2)

        self.client.login(
            testcase_user=self.margaret_user
        )

        resp = self.client.get(
            reverse(
                'core:metadata',
                args=('page', page_1.id)
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(
            resp.status_code, 403
        )

        resp = self.client.get(
            reverse(
                'core:metadata',
                args=('page', page_2.id)
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(
            resp.status_code, 403
        )

        resp = self.client.get(
            reverse(
                'core:metadata',
                args=('node', elizabet_doc.id)
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(
            resp.status_code, 403
        )

        self.client.logout()

        # but elizabet has access
        self.client.login(
            testcase_user=self.elizabet_user
        )

        resp = self.client.get(
            reverse(
                'core:metadata',
                args=('page', page_1.id)
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(
            resp.status_code, 200
        )

        resp = self.client.get(
            reverse(
                'core:metadata',
                args=('page', page_2.id)
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(
            resp.status_code, 200
        )

        resp = self.client.get(
            reverse(
                'core:metadata',
                args=('node', elizabet_doc.id)
            ),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(
            resp.status_code, 200
        )
