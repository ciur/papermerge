from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import TestCase
from papermerge.core.models import KV, Document, Folder, Page
from papermerge.core.models.kvstore import MONEY, TEXT
from papermerge.core.tasks import normalize_pages

User = get_user_model()

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestPage(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin')

    def get_whatever_doc(self):
        return Document.create_document(
            title="kyuss.pdf",
            user=self.user,
            lang="ENG",
            file_name="kyuss.pdf",
            size=1222,
            page_count=3
        )

    def test_language_is_inherited(self):
        """
        Whatever document model has in doc.lang field
        will be inherited by the related page models.
        """
        doc = Document.create_document(
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
        doc = Document.create_document(
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
        doc.pages.all().delete()
        self.assertEqual(
            doc.pages.count(),
            0
        )

    def test_page_matching_search(self):
        doc = self.get_whatever_doc()
        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        result = Page.objects.search("cool")

        self.assertEquals(
            result.count(),
            1
        )

    def test_page_not_matching_search(self):
        doc = self.get_whatever_doc()
        page = Page(
            text="Some cool content in page model",
            user=self.user,
            document=doc
        )
        page.save()
        result = Page.objects.search("andromeda")

        self.assertEquals(
            result.count(),
            0
        )

    def test_normalize_doc_title(self):
        doc = Document.create_document(
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
        doc = self.get_whatever_doc()
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
        doc = Document.create_document(
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

    def test_page_kv_store_get_and_set(self):
        """
        test that kv api works:

            page.kv['shop'] = 'lidl'
            page.kv['price'] = '11.99'
            page.kv['shop'] == 'lidl'
            page.kv['price'] == '11.99'
        """
        doc = self.get_whatever_doc()
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
        doc = self.get_whatever_doc()
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
