import os
import json
from unittest import skip
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from mglib.path import PagePath
from mglib.step import Step

from papermerge.core.auth import create_access
from papermerge.core.models import (
    Page,
    Document,
    Folder,
    Access
)
from papermerge.core.storage import default_storage
from papermerge.core.models.kvstore import (
    TEXT,
    KVStorePage
)

from .utils import (
    create_root_user,
    create_margaret_user,
    create_elizabet_user,
    create_some_doc
)


READ = Access.PERM_READ
WRITE = Access.PERM_WRITE
DELETE = Access.PERM_DELETE

BASE_DIR = os.path.dirname(__file__)


class TestDocumentView(TestCase):

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_index(self):
        self.client.get(
            reverse('index')
        )

    def test_upload(self):
        self.assertEqual(
            Document.objects.count(),
            0
        )
        file_path = os.path.join(
            BASE_DIR,
            "data",
            "berlin.pdf"
        )
        with open(file_path, "rb") as fp:
            self.client.post(
                reverse('core:upload'),
                {
                    'name': 'fred',
                    'file': fp,
                    'language': "eng",
                },
            )

        # Was a document instance created ?
        self.assertEqual(
            Document.objects.count(),
            1
        )

    def test_preview_document_does_not_exist(self):
        ret = self.client.post(
            reverse('core:preview', args=(1, 1)),
        )
        self.assertEqual(
            ret.status_code, 404
        )

    def test_preview(self):
        doc = Document.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        default_storage.copy_doc(
            src=os.path.join(
                BASE_DIR, "data", "berlin.pdf"
            ),
            dst=doc.path.url(),
        )
        ret = self.client.post(
            reverse('core:preview', args=(doc.id, 1, 1))
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        page_path = PagePath(
            document_path=doc.path,
            page_num=1,
            step=Step(1),
            page_count=3
        )
        self.assertTrue(
            os.path.exists(
                default_storage.abspath(page_path.img_url())
            )
        )

    def test_copy_paste(self):
        """
        To my surprise, a nasty bug made his way into copy pasting
        documents feature. When (e.g.) 10 documents were copied
        from one folder A to folder B - only a part of them
        "made it to destination". It kinda looked as if all docs
        were copied... but in reality tree structure undeneath
        went corrupt.
        """
        # where user will paste
        inbox = Folder.objects.create(
            title="Inbox",
            user=self.testcase_user
        )
        # folder with 10 documents
        folder = Folder.objects.create(
            title="Folder",
            user=self.testcase_user
        )
        doc_ids = []
        for index in range(1, 11):
            doc = Document.create_document(
                title=f"andromeda-{index}.pdf",
                user=self.testcase_user,
                lang="ENG",
                file_name=f"andromeda={index}.pdf",
                size=1222,
                page_count=3,
                parent_id=folder.id
            )
            doc_ids.append(doc.id)

        # Without obj.refresh_from_db() test fails!
        folder.refresh_from_db()

        self.assertEqual(
            inbox.get_descendants().count(),
            0
        )

        self.assertEqual(
            folder.get_descendants().count(),
            10
        )
        # copy nodes (place node_ids in current session)
        node_ids = [{'id': doc_id} for doc_id in doc_ids]
        self.client.post(
            reverse('core:cut_node'),
            json.dumps(node_ids),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        # paste nodes to inbox
        self.client.post(
            reverse('core:paste_node'),
            {'parent_id': inbox.id},
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        inbox.refresh_from_db()
        self.assertEqual(
            inbox.get_descendants().count(),
            10
        )
        folder.refresh_from_db()
        self.assertEqual(
            folder.get_descendants().count(),
            0
        )

    @skip("This test fails on Travis-CI only. Investigating...")
    def test_download(self):
        doc = Document.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        default_storage.copy_doc(
            src=os.path.join(
                BASE_DIR, "data", "berlin.pdf"
            ),
            dst=doc.path.url()
        )
        ret = self.client.post(
            reverse('core:document_download', args=(doc.id, ))
        )
        self.assertEqual(
            ret.status_code,
            200
        )

    def test_download_with_wrong_id(self):
        ret = self.client.post(
            reverse(
                'core:document_download',
                # some 'random' number
                args=("198300000002019", )
            )
        )
        self.assertEqual(
            ret.status_code,
            404
        )

    def test_download_hocr(self):
        doc = Document.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )

        default_storage.copy_doc(
            src=os.path.join(
                BASE_DIR, "data", "berlin.pdf"
            ),
            dst=default_storage.abspath(doc.path.url())
        )
        # build page url
        page_path = doc.page_paths[1]

        # just remember that at the end of test
        # copied file must be deteled. (1)
        default_storage.copy_doc(
            src=os.path.join(
                BASE_DIR, "data", "page-1.hocr"
            ),
            dst=default_storage.abspath(page_path.hocr_url())
        )
        ret = self.client.get(
            reverse('core:hocr', args=(doc.id, 1, 1))
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        # Deleting file created at (1)
        os.remove(
            default_storage.abspath(page_path.hocr_url())
        )

    def test_download_hocr_which_does_not_exists(self):
        """
        HOCR might not be available. It is a normal case
        (page OCR task is still in the queue/progress).

        Missing HCOR file => HTTP 404 return code is expected.
        """
        doc = Document.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="ENG",
            file_name="berlin.pdf",
            size=1222,
            page_count=3
        )
        # Doc is available (for get_pagecount on server side).
        default_storage.copy_doc(
            src=os.path.join(
                BASE_DIR, "data", "berlin.pdf"
            ),
            dst=doc.path.url()
        )
        # But HOCR file is missing.
        ret = self.client.get(
            reverse('core:hocr', args=(doc.id, 1, 1))
        )
        self.assertEqual(
            ret.status_code,
            404
        )

    @skip(
        """For unknown to me reason POST redirects to login page..."
        What makes it very strange is that all other tests use test auth
        backend papermerge.test.auth_backends - they skip authentication
        basically; but this test is very stubborn. And worst - in development
        mode this feature does not show any sign of misfunction.
        So, I will just skip it for a while.
        """
    )
    def test_change_document_notes(self):
        doc = Document.create_document(
            title="berlin.pdf",
            user=self.testcase_user,
            lang="eng",
            file_name="berlin.pdf",
            size=1222,
            page_count=1
        )

        doc.notes = "Old note"
        doc.save()

        self.assertEqual(
            doc.notes,
            "Old note"
        )

        page = Page.objects.get(document_id=doc.id)

        # Why? Why to hell is this guy only one in whole test
        # suite which redirects to login page?
        post_url = reverse(
            'boss:core_basetreenode_change', args=(doc.id, )
        )
        ret = self.client.post(
            post_url,
            {
                'page_set-TOTAL_FORMS': 1,
                'page_set-INITIAL_FORMS': 1,
                'page_set-MIN_NUM_FORMS': 0,
                'page_set-MAX_NUM_FORMS': 0,
                'page_set-0-id': page.id,
                'language': 'eng',
                'notes': 'more recent note',
                'title': 'andromeda.pdf',
                '_save': 'Save'
            },
        )
        self.assertEqual(
            ret.status_code,
            302,
            "After saving document wasn't redirected to its parent."
        )

        doc.refresh_from_db()
        self.assertEqual(
            doc.notes,
            "more recent note"
        )


class TestUpdateDocumentMetadataView(TestCase):
    """
    Make sure update/create metadata on a Page - works.
    """

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_update_existing_metadata_value_on_page(self):
        """
        You recognize an update by presense of 'id' key.
        """
        doc = create_some_doc(
            self.testcase_user,
            page_count=1
        )

        doc.kv.update([
            {
                'key': 'license_number',
                'kv_type': TEXT,
            },
            {
                'key': 'holder',
                'kv_type': TEXT,
            },
        ])

        # doc has only one page
        page = Page.objects.get(
            document_id=doc.id
        )
        #
        kv_license = KVStorePage.objects.get(
            page=page,
            key="license_number"
        )
        kv_holder = KVStorePage.objects.get(
            page=page,
            key="holder"
        )
        # update metadata for given page
        post_url = reverse(
            'core:metadata', args=('page', page.id)
        )
        post_data = {
            "kvstore": [{
                "id": kv_license.id,
                "key": "license_number",
                "value": "AM43122101",
                "virtual_value": 0,  # this field will be sanitized
                "kv_inherited": True,
                "kv_type": "text",
                "kv_format": None
            }, {
                "id": kv_holder.id,
                "key": "holder",
                "value": "John Licenseberg",
                "virtual_value": 0,  # this field will be sanitized
                "kv_inherited": True,
                "kv_type": "text",
                "kv_format": None
            }]
        }
        ret = self.client.post(
            post_url,
            json.dumps(post_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )

        page.refresh_from_db()

        # make sure that page's metadata values were
        # updated indeed
        self.assertEqual(
            page.kv['holder'],
            "John Licenseberg"
        )

        self.assertEqual(
            page.kv['license_number'],
            "AM43122101"
        )

    def test_create_metadata_on_page(self):
        """
        You recognize create operation by absence of 'id' key.
        """
        doc = create_some_doc(
            self.testcase_user,
            page_count=1
        )

        # doc has only one page
        page = Page.objects.get(
            document_id=doc.id
        )

        # create metadata for given page
        post_url = reverse(
            'core:metadata', args=('page', page.id)
        )
        post_data = {
            "kvstore": [{
                # note, there is no ID key
                "key": "license_number",
                "value": "AM43122101",
                "virtual_value": 0,  # this field will be sanitized
                "kv_inherited": True,
                "kv_type": "text",
                "kv_format": None
            }, {
                # note, there is no ID key
                "key": "holder",
                "value": "John Licenseberg",
                "virtual_value": 0,  # this field will be sanitized
                "kv_inherited": True,
                "kv_type": "text",
                "kv_format": None
            }]
        }
        ret = self.client.post(
            post_url,
            json.dumps(post_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )

        page.refresh_from_db()

        # make sure that page's metadata values were
        # updated indeed
        self.assertEqual(
            page.kv['holder'],
            "John Licenseberg"
        )

        self.assertEqual(
            page.kv['license_number'],
            "AM43122101"
        )


class TestDocumentAjaxOperationsView(TestCase):
    """
    Tests operations on the document via Ajax e.g.
    edit fields, delete document.
    """

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_update_notes(self):
        """
        You recognize an update by presense of 'id' key.
        """
        doc = create_some_doc(
            self.testcase_user,
            page_count=1
        )
        # update metadata for given page
        patch_url = reverse(
            'core:document', args=(doc.id,)
        )
        patch_data = {
            "notes": "Test note"
        }
        ret = self.client.patch(
            patch_url,
            json.dumps(patch_data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )

        doc.refresh_from_db()

        self.assertEqual(
            doc.notes,
            "Test note",
            "document notes field was not updated."
        )

    def test_delete_document(self):
        """
        You recognize an update by presense of 'id' key.
        """
        doc = create_some_doc(
            self.testcase_user,
            page_count=1
        )
        # update metadata for given page
        url = reverse(
            'core:document', args=(doc.id,)
        )
        ret = self.client.delete(
            url,
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )

        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(id=doc.id)


class TestDocumentDownload(TestCase):

    def setUp(self):

        self.root_user = create_root_user()
        self.margaret_user = create_margaret_user()
        self.elizabet_user = create_elizabet_user()
        self.client = Client()

    def test_user_download_document(self):
        """
        If user has read access to the document
        (even if he/she is not the owner of the document), then
        he/she must be able to download it.

        Scenario:
            admin user creates a document and assigns
            read only access for margaret
            (thus, root is the owner of the document).

        Expected:

            Margaret and root user must be able to download the document.
            Elizabet on the other hand - must not have access to the document
            (she was not assigned permissions for that)
        """
        document_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )

        doc = Document.create_document(
            user=self.root_user,
            title='berlin.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin.pdf',
            page_count=3
        )
        # copy document from its test/data place
        # to the media storage, as if document was uploaded.
        default_storage.copy_doc(
            src=document_path,
            dst=doc.path.url(),
        )
        create_access(
            node=doc,
            name=self.margaret_user.username,
            model_type=Access.MODEL_USER,
            access_type=Access.ALLOW,
            access_inherited=False,
            permissions={
                READ: True
            }  # allow read access to margaret
        )
        self.client.login(
            testcase_user=self.margaret_user
        )

        url = reverse(
            'core:document_download', args=(doc.id,)
        )

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            200
        )

        # also, root/admin must be able to download it
        self.client.logout()
        self.client.login(
            testcase_user=self.root_user
        )

        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            200
        )

        self.client.logout()

        # for elizabet on the other hand, access is forbidden.
        self.client.login(testcase_user=self.elizabet_user)
        ret = self.client.get(url)

        self.assertEqual(
            ret.status_code,
            403
        )
