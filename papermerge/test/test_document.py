import os
from pathlib import Path

from django.test import TestCase
from django.core.exceptions import ValidationError

from papermerge.core.import_pipeline import go_through_pipelines
from papermerge.core.models import Document, Folder, Automate
from papermerge.test.utils import create_root_user

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestDocument(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_tree_path(self):
        """
        Create following structure:
            Folder A > Folder B > Document C
        and check ancestors of Document C
        """

        folder_a = Folder.objects.create(
            title="folder_a",
            user=self.user,
            parent_id=None
        )
        folder_a.save()

        folder_b = Folder.objects.create(
            title="folder_b",
            user=self.user,
            parent_id=folder_a.id
        )
        folder_b.save()

        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder_b.id,
            page_count=5,
        )
        ancestors = [
            [node.title, node.id]
            for node in doc.get_ancestors(include_self=True)
        ]
        self.assertListEqual(
            ancestors,
            [
                ['folder_a', folder_a.id],
                ['folder_b', folder_b.id],
                ['document_c', doc.id]
            ]
        )
        self.assertEqual(
            doc.pages.count(),
            5
        )

    def test_delete_document_with_parent(self):
        """
        Document D is child of folder F.
        Deleting document D, will result in... well...
        no more D around, but F still present.
        """
        folder = Folder.objects.create(
            user=self.user,
            title="F"
        )

        doc = Document.objects.create_document(
            title="andromeda.pdf",
            user=self.user,
            lang="ENG",
            file_name="andromeda.pdf",
            size=1222,
            page_count=3
        )
        doc.parent = folder
        doc.save()
        folder.save()
        count = folder.get_children().count()
        self.assertEqual(
            count,
            1,
            f"Folder {folder.title} has {count} children"
        )
        self.assertEqual(
            doc.pages.count(),
            3
        )

        doc.delete()

        self.assertEqual(
            folder.get_children().count(),
            0,
        )

        with self.assertRaises(Document.DoesNotExist):
            Document.objects.get(title="D")

    def test_import_file(self):
        src_file_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )

        with open(src_file_path, 'rb') as fp:
            src_file = fp.read()

        init_kwargs = {'payload': src_file, 'processor': 'TEST'}
        apply_kwargs = {'skip_ocr': True, 'name': "berlin.pdf"}

        self.assertIsNotNone(go_through_pipelines(
            init_kwargs=init_kwargs, apply_kwargs=apply_kwargs))

        self.assertEqual(
            Document.objects.filter(title="berlin.pdf").count(),
            1,
            "Document berlin.pdf was not created."
        )

    def test_update_text_field(self):
        """
        basic test for doc.update_text_field()
        """
        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=None,
            page_count=5,
        )
        doc.update_text_field()

    def test_delete_pages(self):
        # Create a document with two pages
        src_file_path = os.path.join(
            BASE_DIR, "data", "berlin.pdf"
        )

        with open(src_file_path, 'rb') as fp:
            src_file = fp.read()

        init_kwargs = {'payload': src_file, 'processor': 'TEST'}
        apply_kwargs = {'skip_ocr': True, 'name': "berlin.pdf"}
        self.assertIsNotNone(go_through_pipelines(
            init_kwargs=init_kwargs, apply_kwargs=apply_kwargs))

        doc = Document.objects.get(title="berlin.pdf")
        self.assertEqual(
            doc.page_count,
            2
        )
        # initial version of any document is 0
        self.assertEqual(
            doc.version,
            0
        )

        doc.delete_pages(
            page_numbers=[1],
            skip_migration=True
        )

        self.assertEqual(
            doc.page_count,
            1
        )

        self.assertEqual(
            doc.pages.count(),
            1
        )

        # version should have been incremented
        self.assertEqual(
            doc.version,
            1
        )

    def test_document_inherits_kv_from_parent_folder(self):
        """
        Newly added focuments into the folder will inherit folder's
        kv metadata.
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
                    'kv_type': 'text',
                    'kv_format': ''
                },
                {
                    'key': 'total',
                    'kv_type': 'money',
                    'kv_format': 'dd.cc'
                }
            ]
        )
        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=top.id,
            page_count=5,
        )
        doc.save()
        self.assertEqual(2, doc.kv.count())
        self.assertEqual(
            set(
                doc.kv.typed_keys()
            ),
            set(
                top.kv.typed_keys()
            )
        )

    def test_document_moved_into_other_folder_inherits_kv(self):
        """
        When a Document (e.g. named doc) is moved from one folder F1
        into another F2, then all metadata keys (and metadata values)
        of document doc may be are deleted and inherited from parent.
        'May be deleted' because this replacement of metadata will
        not happen if new parent folder (F2) has same metadata keys
        as document doc.
        """
        f1 = Folder.objects.create(
            title="F1",
            user=self.user,
        )
        f1.save()
        f2 = Folder.objects.create(
            title="F2",
            user=self.user,
        )
        f2.save()
        f2.kv.update(
            [{'key': 'shop'}, {'key': 'total'}]
        )
        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=f1.id,
            page_count=5,
        )
        doc.save()
        self.assertEqual(0, doc.kv.count())

        # move document into the new parent
        Document.objects.move_node(doc, f2)

        # assert that metakeys were updated
        self.assertEqual(2, doc.kv.count())
        self.assertEqual(
            set(
                doc.kv.keys()
            ),
            set(
                f2.kv.keys()
            )
        )

        # similarly, pages will inherit kv from their parent
        # document
        page = doc.pages.first()
        # assert that metakeys were updated
        self.assertEqual(2, page.kv.count())
        self.assertEqual(
            set(
                doc.kv.keys()
            ),
            set(
                page.kv.keys()
            )
        )

    def test_assign_tags_from_automate_instance(self):
        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            page_count=5,
        )

        dst_folder = Folder.objects.create(
            title="destination Folder",
            user=self.user
        )

        auto = Automate.objects.create(
            name="whatever",
            match="XYZ",
            matching_algorithm=Automate.MATCH_ALL,
            is_case_sensitive=False,  # i.e. ignore case
            user=self.user,
            dst_folder=dst_folder
        )

        auto.tags.add(
            'invoice',
            'tags',
            tag_kwargs={'user': self.user}
        )

        doc.add_tags(auto.tags.all())

        self.assertEquals(
            doc.tags.count(),
            2
        )

        self.assertEquals(
            set([tag.name for tag in doc.tags.all()]),
            set([tag.name for tag in auto.tags.all()])
        )

    def test_folder_validation_against_xss_titles(self):

        folder_a = Folder(
            title="XSS Folder<script>alert('XSS');</script>",
            user=self.user,
            parent_id=None
        )

        with self.assertRaises(ValidationError):
            folder_a.full_clean()

        folder_b = Folder(
            title="XSS<script></script>",
            user=self.user,
            parent_id=None
        )

        with self.assertRaises(ValidationError):
            folder_b.full_clean()
