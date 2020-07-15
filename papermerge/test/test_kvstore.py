from pathlib import Path

from django.test import TestCase
from papermerge.core.models import Document, Folder
from papermerge.test.utils import create_root_user
from papermerge.core.models.kvstore import (
    compute_virtual_value,
    MONEY,
    NUMERIC,
    DATE
)

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
        doc = Document.create_document(
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

