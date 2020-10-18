from pathlib import Path

from django.test import TestCase

from papermerge.core.models import Document, Folder, KV, Page
from papermerge.test.utils import create_root_user
from papermerge.core.models.kvstore import (
    compute_virtual_value,
    TEXT,
    MONEY,
    NUMERIC,
    DATE
)

from .utils import create_some_doc

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestComputeVirtualValue(TestCase):
    """
    Asserts correctness of compute_virtual_value.
    Virtual value is scalar (integer number) used for metadata sorting.
    """

    def test_date_type(self):

        vv1 = compute_virtual_value(
            kv_type=DATE,
            kv_format='dd.mm.yy',
            value='04.05.20'
        )

        vv2 = compute_virtual_value(
            kv_type=DATE,
            kv_format='dd.mm.yy',
            value='05.06.20'
        )

        self.assertTrue(
            vv2 > vv1,
            f"Assertion {vv2} > {vv1} failed."
        )

    def test_empty_date_type(self):
        vv1 = compute_virtual_value(
            kv_type=DATE,
            kv_format='dd.mm.yy',
            value=''  # empty date
        )

        vv2 = compute_virtual_value(
            kv_type=DATE,
            kv_format='dd.mm.yy',
            value=None
        )
        # in both cases virtual value is expected to be 0
        self.assertEqual(vv1, 0)
        self.assertEqual(vv2, 0)

    def test_money_type(self):

        vv1 = compute_virtual_value(
            kv_type=MONEY,
            kv_format='dd.cc',
            value='45.06'
        )

        vv2 = compute_virtual_value(
            kv_type=MONEY,
            kv_format='dd.cc',
            value='60.20'
        )

        self.assertTrue(
            vv2 > vv1,
            f"Assertion {vv2} > {vv1} failed."
        )

        vv1 = compute_virtual_value(
            kv_type=MONEY,
            kv_format='dd,cc',
            value='45.00'
        )

        vv2 = compute_virtual_value(
            kv_type=MONEY,
            kv_format='dd,cc',
            value='46.00'
        )

        self.assertTrue(
            vv2 > vv1,
            f"Assertion {vv2} > {vv1} failed."
        )

    def test_numeric_type(self):

        vv1 = compute_virtual_value(
            kv_type=NUMERIC,
            kv_format='dddd',
            value='4500'
        )

        vv2 = compute_virtual_value(
            kv_type=NUMERIC,
            kv_format='dddd',
            value='4600'
        )

        self.assertTrue(
            vv2 > vv1,
            f"Assertion {vv2} > {vv1} failed."
        )


class TestKVPropagation(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_metadata_created_on_existing_folder_document_structure(self):
        """
        Consider following folder structure:

                Home
                 |
                Folder_A
                 |
                document.pdf

        1. User adds metadata named price (of money type with format 'dd,cc').
         Notice that at the time of adding metadata - document.pdf
         already exists in Folder_A.

        2. Expected:
            a. document.pdf inherits price metadata
            b. all pages of document.pdf inherit price metadata as well
            c. metadata is inherited with correct format/type
        """
        folder_A = Folder.objects.create(
            title="folder_A",
            user=self.user
        )
        doc = Document.objects.create_document(
            title="document.pdf",
            file_name="document.pdf",
            size='1989',
            lang='DEU',
            user=self.user,
            parent_id=folder_A.id,  # document.pdf is inside folder_A
            page_count=5,
        )
        doc.save()

        folder_A = Folder.objects.get(id=folder_A.id)

        self.assertEqual(
            folder_A.get_children().count(),
            1
        )
        # attach/add metadata to the folder_A
        folder_A.kv.update(
            [
                {
                    'key': 'price',
                    'kv_type': MONEY,
                    'kv_format': 'dd,cc'
                }
            ]
        )
        # metadata was added to the folder_A
        self.assertEqual(
            folder_A.kv.all().count(),
            1
        )
        document_kvs = doc.kv.all()

        # document inherited metadata
        self.assertEqual(
            document_kvs.count(),
            1
        )
        # and document's metadata is of correct format
        self.assertEqual(
            document_kvs[0].kv_type,
            MONEY
        )

        self.assertEqual(
            document_kvs[0].kv_format,
            "dd,cc"
        )
        # now check if metadata was propagated to first page
        page = doc.pages.first()
        page_kv = page.kv.all()
        self.assertEqual(
            page_kv.count(),
            1,
            "Metadata was not propagated to document's page"
        )
        # and test if metadata has correct format
        self.assertEqual(
            page_kv[0].kv_type,
            MONEY
        )

        self.assertEqual(
            page_kv[0].kv_format,
            "dd,cc"
        )

    def test_kv_assignment_of_empty_values(self):
        """
        Assign empty value for kv label date on a document
        """
        doc = create_some_doc(
            self.user
        )

        # attach/add metadata to the document_A
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

        self.assertFalse(
            doc.kv['date']
        )

        doc.kv['date'] = '23.07.20'
        # reload doc from db
        doc = Document.objects.get(id=doc.id)
        self.assertEqual(
            doc.kv['date'], '23.07.20'
        )
        # try empty value for date
        doc.kv['date'] = None
        doc = Document.objects.get(id=doc.id)
        self.assertFalse(
            doc.kv['date']
        )

    def test_kv_assignment_on_document_pages(self):
        """
        Assign metadata values on document pages
        """
        doc = create_some_doc(
            self.user, page_count=2
        )

        doc.kv.update(
            [
                {
                    'key': 'date',
                    'kv_type': DATE,
                    'kv_format': 'dd.mm.yy',
                }
            ]
        )

        extraction_result = {
            'date': '23.07.20'
        }

        doc.assign_kv_values(extraction_result)
        doc = Document.objects.get(id=doc.id)

        self.assertEqual(
            doc.kv['date'],
            '23.07.20'
        )

        # and same value must be present in both pages'
        # metadata
        self.assertEqual(
            doc.pages.all()[0].kv['date'],
            '23.07.20'
        )

        self.assertEqual(
            doc.pages.all()[1].kv['date'],
            '23.07.20'
        )

    def test_update_kv_on_folder(self):
        """
        Folder with X has one metadata key=x of type text.
        Folder X contains one document - doc.
        doc1 has value for the key x => 1:

            doc.kv[x] == 1
            doc.kv[y] - does not exist at this point!

        When user adds new key=y on folder X, document doc1 must preserve
        existing values for key x:

            doc.kv[x] == 1 must still be true
            doc.kv[y] -> exists, but it is empty!
        """
        folder_X = Folder.objects.create(
            title="X",
            user=self.user
        )
        doc = Document.objects.create_document(
            title="document.pdf",
            file_name="document.pdf",
            size='1989',
            lang='DEU',
            user=self.user,
            page_count=5,
            parent_id=folder_X.id
        )
        doc.save()

        folder_X.refresh_from_db()

        folder_X.kv.update(
            [
                {
                    'key': 'x',
                    'kv_type': TEXT,
                }
            ]
        )
        self.assertEqual(
            folder_X.kv.all().count(),
            1
        )

        self.assertEqual(
            doc.kv.all().count(),
            1
        )
        doc.assign_kv_values({'x': '10'})

        self.assertEqual(doc.kv['x'], '10')

        folder_X.refresh_from_db()
        folder_X.kv.update(
            [
                {
                    'key': 'y',
                    'kv_type': TEXT,
                },
                {
                    'key': 'x',
                    'kv_type': TEXT,
                }
            ]
        )
        self.assertEqual(
            folder_X.kv.all().count(),
            2
        )

        self.assertEqual(
            doc.kv.all().count(),
            2
        )
        doc.refresh_from_db()
        self.assertEqual(doc.kv['x'], '10')

        page = Page.objects.get(document=doc, number=1)

        self.assertEqual(
            page.kv['x'],
            '10'
        )

        # key 'y' exists but it is empty/None
        self.assertIsNone(doc.kv['y'])

        # key 'z' does not exits
        with self.assertRaises(KV.MetadataKeyDoesNotExist):
            self.assertIsNone(doc.kv['z'])
