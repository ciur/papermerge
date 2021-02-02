import os
from pathlib import Path

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from papermerge.core.models import (
    KV,
    Document,
    Folder,
    Page,
    KVStorePage,
    KVStoreNode
)
from papermerge.core.models.kvstore import MONEY, TEXT, DATE
from papermerge.core.tasks import normalize_pages
from papermerge.core.storage import default_storage
from papermerge.core.models.page import get_pages
from papermerge.core.models.folder import get_inbox_children

from .utils import (
    create_root_user,
    create_some_doc
)

User = get_user_model()

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestPage(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_language_is_inherited(self):
        """
        Whatever document model has in doc.lang field
        will be inherited by the related page models.
        """
        doc = Document.objects.create_document(
            title="kyuss.pdf",
            user=self.user,
            lang="ENG",
            file_name="kyuss.pdf",
            size=1222,
            page_count=3
        )

        doc.save()

        self.assertEqual(
            doc.pages.count(),
            3
        )

        langs = [
            page.lang for page in doc.pages.all()
        ]

        self.assertEqual(
            ['ENG', 'ENG', 'ENG'],
            langs
        )

    def test_recreate_page_models(self):
        doc = create_some_doc(self.user, page_count=3)

        doc.save()

        self.assertEqual(
            doc.pages.count(),
            3
        )
        doc.pages.all().delete()
        self.assertEqual(
            doc.pages.count(),
            0
        )

    def test_page_matching_search(self):
        doc = create_some_doc(self.user)
        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        result = Page.objects.search("cool")

        self.assertEqual(
            result.count(),
            1
        )

    def test_page_not_matching_search(self):
        doc = create_some_doc(self.user)
        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        result = Page.objects.search("andromeda")

        self.assertEqual(
            result.count(),
            0
        )

    def test_normalize_doc_title(self):
        doc = Document.objects.create_document(
            title="kyuss.pdf",
            user=self.user,
            lang="ENG",
            file_name="kyuss.pdf",
            size=1222,
            page_count=3
        )

        doc.save()
        # simulate a singnal trigger
        normalize_pages(doc)

        first_page = doc.pages.first()
        self.assertEqual(
            first_page.norm_doc_title,
            "kyuss.pdf"
        )

        result = Page.objects.search("kyuss")
        # doc has 3 pages, thus keyword kyuss will
        # match 3 pages (because of normalized page.norm_doc_title).
        self.assertEqual(
            result.count(),
            3
        )

    def test_basic_kvstore_for_page(self):
        doc = create_some_doc(self.user)
        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        self.assertEqual(
            0,
            page.kvstore.count()
        )
        page.kv.add(key="shop")
        self.assertEqual(
            1,
            page.kvstore.count()
        )

    def test_page_inherits_kv_from_document(self):
        """
        Given a folder, say groceries with
        kv: "shop", "price", "date"
        a document created in that folder will have
        pages's kv data "shop", "price", "date" as well.

        KV inheritance flows like this:

            Folder -> Document -> Page
        """
        top = Folder.objects.create(
            title="top",
            user=self.user,
        )
        top.save()
        top.kv.update(
            [
                {
                    'key': 'shop',
                    'kv_type': TEXT,
                    'kv_format': ''
                },
                {
                    'key': 'total',
                    'kv_type': MONEY,
                    'kv_format': 'dd,cc'
                }
            ]
        )
        doc = Document.objects.create_document(
            title="kyuss.pdf",
            user=self.user,
            lang="ENG",
            file_name="kyuss.pdf",
            size=1222,
            parent_id=top.id,
            page_count=3
        )
        page = doc.pages.first()

        self.assertEqual(
            2,
            doc.kv.count(),
            "Document does not have two metakeys associated"
        )

        self.assertEqual(
            2,
            page.kv.count(),
            "Page does not have two metakeys associated"
        )

        self.assertEqual(
            set(
                page.kv.typed_keys()
            ),
            set(
                top.kv.typed_keys()
            )
        )

    def test_page_inherits_kv_from_document_2(self):
        """
        KV inheritance:

            Document -> Page
        1. Create 2 pages document
        2. Assign metadata to the document
        3. Expected:
            both pages will have same metadata keys as document.
        """
        doc = create_some_doc(self.user, page_count=2)

        # create one metadata key
        doc.kv.update(
            [
                {
                    'key': 'date',
                    'kv_type': DATE,
                    'kv_format': 'dd.mm.yy',
                }
            ]
        )

        doc.save()

        self.assertEqual(
            1,
            doc.kv.count(),
            "Document does not one metakey associated"
        )

        self.assertEqual(
            1,
            doc.pages.first().kv.count(),
            "Page does not have one metakey associated"
        )

        self.assertEqual(
            1,
            doc.pages.last().kv.count(),
            "Page does not have one metakey associated"
        )

    def test_page_kv_keys_are_updated_if_key_of_document_is_updated(self):
        """
        If kv keys are updated/changed on a document - respetive
        changes must be reflected on the associated page model as well.
        """
        doc = create_some_doc(self.user, page_count=2)

        # create one metadata key
        doc.kv.update(
            [
                {
                    'key': 'date',
                    'kv_type': DATE,
                    'kv_format': 'dd.mm.yy',
                }
            ]
        )

        doc.save()

        # retrieve associated kv
        kv_doc = KVStoreNode.objects.get(node=doc)
        self.assertEqual(
            kv_doc.kv_format,
            "dd.mm.yy"
        )

        page_1 = Page.objects.get(document=doc, number=1)

        # retrieve associated kv
        kv_page = KVStorePage.objects.get(page=page_1)
        self.assertEqual(
            kv_page.kv_format,
            "dd.mm.yy"
        )

        # update document key format
        doc.kv.update(
            [
                {
                    'id': kv_doc.id,
                    'key': 'date',
                    'kv_type': DATE,
                    'kv_format': 'dd.mm.yyyy',
                }
            ]
        )

        kv_doc.refresh_from_db()
        self.assertEqual(
            kv_doc.kv_format,
            "dd.mm.yyyy"
        )

        # same for page model - changes should take effect
        kv_page.refresh_from_db()
        self.assertEqual(
            kv_page.kv_format,
            "dd.mm.yyyy"
        )

    def test_page_kv_keys_are_updated_if_key_of_folder_is_updated(self):
        """
        If kv keys are updated/changed on a folder - respetive
        changes must be reflected on the associated pages model as well
        (through documents which a part of the folder).
        """
        top = Folder.objects.create(
            title="top",
            user=self.user,
        )
        top.save()
        doc = create_some_doc(self.user, page_count=2)
        doc.parent = top
        doc.save()

        # create one metadata key
        top.kv.update(
            [
                {
                    'key': 'date',
                    'kv_type': DATE,
                    'kv_format': 'dd.mm.yy',
                }
            ]
        )

        top.save()

        # retrieve associated kv
        kv_top = KVStoreNode.objects.get(node=top)
        self.assertEqual(
            kv_top.kv_format,
            "dd.mm.yy"
        )

        page_1 = Page.objects.get(document=doc, number=1)

        # retrieve associated kv
        kv_page = KVStorePage.objects.get(page=page_1)
        self.assertEqual(
            kv_page.kv_format,
            "dd.mm.yy"
        )

        # update document key format
        top.kv.update(
            [
                {
                    'id': kv_top.id,
                    'key': 'date',
                    'kv_type': DATE,
                    'kv_format': 'dd.mm.yyyy',
                }
            ]
        )

        kv_top.refresh_from_db()
        self.assertEqual(
            kv_top.kv_format,
            "dd.mm.yyyy"
        )

        # same for page model - changes should take effect
        kv_page.refresh_from_db()
        self.assertEqual(
            kv_page.kv_format,
            "dd.mm.yyyy"
        )

    def test_page_kv_store_get_and_set(self):
        """
        test that kv api works:

            page.kv['shop'] = 'lidl'
            page.kv['price'] = '11.99'
            page.kv['shop'] == 'lidl'
            page.kv['price'] == '11.99'
        """
        doc = create_some_doc(self.user)

        page = Page(
            text="Receipt page",
            user=self.user,
            document=doc
        )
        page.save()
        # set page's kv to shop and price
        page.kv.update(
            [{'key': 'shop'}, {'key': 'price'}]
        )
        # now following setters and getters should work
        page.kv['shop'] = 'lidl'
        page.kv['price'] = '42.50'

        page = Page.objects.get(text="Receipt page")

        self.assertEqual(
            page.kv['shop'],
            'lidl'
        )

        self.assertEqual(
            page.kv['price'],
            '42.50'
        )

        with self.assertRaises(KV.MetadataKeyDoesNotExist):
            page.kv['blah'] = '10'

        with self.assertRaises(KV.MetadataKeyDoesNotExist):
            page.kv['blah']

    def test_page_kv_stores_value(self):
        doc = create_some_doc(self.user)

        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        page.kv.update(
            [
                {
                    'key': 'shop',
                    'kv_type': TEXT,
                    'kv_format': '',
                    'value': 'lidl'
                },
                {
                    'key': 'price',
                    'kv_type': MONEY,
                    'kv_format': 'dd,cc',
                    'value': '10,99'
                }
            ]
        )
        page = Page.objects.get(id=page.id)
        kvstore_set = set([kv.value for kv in page.kv.all()])

        self.assertEqual(
            kvstore_set,
            set(["10,99", "lidl"])
        )

        # now update value of key=shop
        # get ID's of newly created KVStoreNode instances
        _kv_list_of_dicts = [
            {
                'key': item.key,
                'id': item.id,
                'kv_type': item.kv_type,
                'kv_format': item.kv_format,
                'value': item.value
            } for item in page.kv.all()
        ]
        # find key titled 'total', and rename it to 'total_price'
        for obj_with_lidl_value in _kv_list_of_dicts:
            if obj_with_lidl_value['value'] == 'lidl':
                break
        else:
            obj_with_lidl_value = None

        if obj_with_lidl_value:
            obj_with_lidl_value['value'] = 'rewe'

        page.kv.update(_kv_list_of_dicts)
        kvstore_set = set([kv.value for kv in page.kv.all()])
        self.assertEqual(
            kvstore_set,
            set(["10,99", "rewe"])
        )

    def test_pages_all_returns_pages_ordered(self):
        """
        document.pages.all() must always return ordered
        pages (ordered by page.number attribute).
        Otherwise frontend might sporadically display pages on left
        side bar - randomly ordered
        """
        doc = create_some_doc(self.user, page_count=3)
        # similar code to create_pages. However
        # it forces random order page creation.
        doc.pages.all().delete()

        for page_index in [3, 2, 1]:
            preview = reverse(
                'core:preview',
                args=[doc.id, 800, page_index]
            )

            doc.pages.create(
                user=self.user,
                number=page_index,
                image=preview,
                lang=doc.lang,
                page_count=3
            )

        doc.refresh_from_db()
        pages_numbers = [
            page.number for page in doc.pages.all()
        ]

        self.assertEqual(
            pages_numbers,
            [1, 2, 3]
        )

    def test_documents_retains_per_page_metadata_after_page_delete(self):
        """
        DocM is a document with 3 pages. DocM has two metadata fields
        associated X and Y. Field has a value x=10 and y=20.

        Second page of the document DocM is deleted.
        Expected:
            document values of metadata fields X and Y should be preserverd:
            DocX.M is still 10 and DocM.Y is still 20.

        Important!

        In document browser and document viewer
        if user does not explicitely select a page, by default
        metadata associated with first page of respective document
        is returned.
        """
        document_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )
        docm = Document.objects.create_document(
            user=self.user,
            title='berlin.pdf',
            size=os.path.getsize(document_path),
            lang='deu',
            file_name='berlin.pdf',
            parent_id=None,
            page_count=3
        )

        default_storage.copy_doc(
            src=document_path,
            dst=docm.path().url(),
        )

        for number in range(1, 4):
            page = docm.pages.get(number=number)
            # filesystem absolute path /home/eugen/x/y/
            fs_abs_path = default_storage.abspath(
                page.path().url()
            )
            # filesystem absolute dir
            fs_abs_dir = os.path.dirname(
                fs_abs_path
            )
            Path(
                fs_abs_dir
            ).mkdir(parents=True, exist_ok=True)
            # create an empty file
            open(fs_abs_path, "w+")

        # indeed, docm has 3 pages
        self.assertEqual(
            docm.pages.count(),
            3
        )
        docm.kv.update([
            {
                'key': 'X',
                'kv_type': TEXT,
            },
            {
                'key': 'Y',
                'kv_type': TEXT,
            }

        ])
        # In document browser and document viewer
        # if user does not explicitely select a document, by default
        # metadata associated with first page of respective document
        # is returned
        page = docm.pages.get(number=1)
        page.kv['X'] = 10
        page.kv['Y'] = 20

        page.refresh_from_db()

        self.assertEqual(
            page.kv['X'],
            '10'
        )

        self.assertEqual(
            page.kv['Y'],
            '20'
        )

        # Even if user deletes second page, all data (incl. metadata)
        # associated ramaining page (first and last)
        # MUST be preserved!
        docm.delete_pages([2])

        page = docm.pages.get(number=1)

        self.assertEqual(
            page.kv['X'],
            '10'
        )
        self.assertEqual(
            page.kv['Y'],
            '20'
        )

    def test_get_pages(self):
        inbox, _ = Folder.objects.get_or_create(
            title=Folder.INBOX_NAME,
            user=self.user
        )

        folder_in_inbox, _ = Folder.objects.get_or_create(
            title="folder_in_inbox",
            user=self.user,
            parent_id=inbox.id
        )

        Document.objects.create_document(
            title="Document 1",
            file_name="invoice-1.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=inbox.id,
            page_count=1,
        )

        Document.objects.create_document(
            title="Document 2",
            file_name="invoice-2.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder_in_inbox.id,
            page_count=1,
        )

        # for all Page models add some content
        for page in Page.objects.all():
            page.text = "some content"
            page.save()

        pages = get_pages(
            get_inbox_children(self.user),
            include_pages_with_empty_text=False
        )

        # returned only Document 1 - as direct child of "inbox" folder
        self.assertEquals(
            pages.count(),
            1
        )
        self.assertEquals(
            pages.first().document.title,
            "Document 1"
        )

    def test_get_pages_runs_ok_when_inbox_is_empty(self):
        inbox, _ = Folder.objects.get_or_create(
            title=Folder.INBOX_NAME,
            user=self.user
        )

        get_pages(
            get_inbox_children(self.user),
            include_pages_with_empty_text=False
        )
