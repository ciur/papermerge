from django.test import TestCase
from papermerge.core.models import Document, Folder
from papermerge.test.utils import create_root_user


class TestNode(TestCase):

    """
    Both methods - is_folder and is_document
    are defined on the node i.e. on BaseTreeNode model
    """

    def setUp(self):
        self.user = create_root_user()

    def test_node_is_folder(self):
        node = Folder.objects.create(
            title="folder_a",
            user=self.user,
            parent_id=None
        )
        node.save()

        self.assertTrue(
            node.is_folder()
        )
        self.assertFalse(
            node.is_document()
        )

    def test_node_is_document(self):
        node = Document.create_document(
            title="document_node",
            file_name="document_node.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            page_count=5,
        )
        node.save()

        self.assertTrue(
            node.is_document()
        )
        self.assertFalse(
            node.is_folder()
        )
