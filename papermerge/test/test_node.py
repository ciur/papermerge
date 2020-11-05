from django.test import TestCase
from papermerge.core.models import Document, Folder, BaseTreeNode
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
        node = Document.objects.create_document(
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


class TestRecursiveDelete(TestCase):
    """
    Dedicated TestCase for very suble bug.

    There 2 empty folders: A and B:
                   Home
                A         B

    User uploads document to folder A:
                   Home
                A         B
                |
             document.pdf

    User moves empty folder B (Cut -> Paste) into A:
                 Home
                   |
                   A
                 /   \
                /     \
        document.pdf   B

    Expected: User can delete folder A (
        recursively this must delete document.pdf and folder B)
    Actual: When deleting folder A - there is a foreign key constrain error
    """

    def setUp(self):
        self.user = create_root_user()

    def test_delete_folder_with_document(self):

        folder_A = Folder.objects.create(
            title="A",
            user=self.user
        )

        folder_B = Folder.objects.create(
            title="B",
            user=self.user,
        )

        doc = Document.objects.create_document(
            title="document.pdf",
            file_name="document.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder_A.id,
            page_count=5,
        )
        doc.save()

        BaseTreeNode.objects.move_node(folder_B, folder_A)

        folder_A.refresh_from_db()
        # at this point, folder_A will have 2 descendants:
        #   * folder B
        #   * document.pdf
        descendants_count = folder_A.get_descendants(
            include_self=False
        ).count()

        self.assertEqual(
            2,
            descendants_count
        )
        folder_A.delete()

        # by now everything should be deleted
        self.assertEqual(
            0,
            BaseTreeNode.objects.count()
        )

    def test_delete_folder_with_recentely_moved_in_descendant(self):
        """
        Related to test_delete_folder_with_document.
        This test assert that user can delete folders with recently
        moved in folders.
        There 2 empty folders: A and B:
                       Home
                    A         B

        User moves empty folder B (Cut -> Paste) into A:
                     Home
                       |
                       A
                       |
                       |
                       B

        Expected: User can delete folder A (
            recursively this must delete folder B)

        """
        folder_A = Folder.objects.create(
            title="A",
            user=self.user
        )

        folder_B = Folder.objects.create(
            title="B",
            user=self.user,
        )

        Folder.objects.move_node(folder_B, folder_A)

        folder_A.refresh_from_db()
        # at this point, folder_A will have 2 descendants:
        #   * folder B
        #   * document.pdf
        descendants_count = folder_A.get_descendants(
            include_self=False
        ).count()

        self.assertEqual(
            1,
            descendants_count
        )

        # no exception should be raised here.
        folder_A.delete()
        # no folders left
        self.assertEqual(
            0,
            Folder.objects.count()
        )

    def test_delete_folders_and_documents_recursively(self):
        """
        User should be able to delete folder A in following structure:
                     Home
                      |
                      |
                      A
                     / \
                    /   \
                doc1.pdf subfolder
                           / \
                          /   \
                         B     doc2.pdf

        basically this test asserts correct functionality of
        node/folder queryset delete function
        """
        folder_A = Folder.objects.create(
            title="A",
            user=self.user
        )

        subfolder = Folder.objects.create(
            title="subfolder",
            user=self.user,
            parent_id=folder_A.id
        )

        doc = Document.objects.create_document(
            title="document.pdf",
            file_name="document.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder_A.id,
            page_count=5,
        )
        doc.save()

        Folder.objects.create(
            title="B",
            user=self.user,
            parent_id=subfolder.id
        )

        doc = Document.objects.create_document(
            title="document.pdf",
            file_name="document.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=subfolder.id,
            page_count=5,
        )
        doc.save()

        self.assertEqual(
            5,
            BaseTreeNode.objects.count()
        )

        # no exceptions here
        folder_A.delete()

        self.assertEqual(
            0,
            BaseTreeNode.objects.count()
        )
