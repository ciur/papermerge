from pathlib import Path

from django.test import TestCase
from papermerge.core.models import Folder
from papermerge.core.models.kvstore import KVCompKeyLengthMismatch
from papermerge.test.utils import create_root_user

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent


class TestFolder(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_delete_parent_deletes_nested_folder_as_well(self):
        """
        If folder C is child of folder P, then when
        deleting P - C will be deleted as well
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )

        Folder.objects.create(
            title="C",
            user=self.user,
            parent=p
        )

        p = Folder.objects.get(title="P")
        self.assertEqual(p.get_children().count(), 1)

        Folder.objects.get(title="P").delete()

        with self.assertRaises(Folder.DoesNotExist):
            Folder.objects.get(title="C")

    def test_delete_nested_folder_does_not_delete_parent(self):
        """
        If folder C is child of folder P, then when
        deleting C - P should not be deleted
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )

        Folder.objects.create(
            title="C",
            user=self.user,
            parent=p
        )

        p = Folder.objects.get(title="P")
        self.assertEqual(p.get_children().count(), 1)

        Folder.objects.get(title="C").delete()

        try:
            Folder.objects.get(title="P")
        except Folder.DoesNotExist:
            self.fail(
                "Parent folder was deleted when child"
                " deletion only was intended"
            )

    def test_basic_kvstore_for_folder(self):
        """
        kvstore is per node: i.e. per folder and per document
        f = Folder()
        f.kv = instance of KVNode, which operates on f.kvstore
        f.kvstore = QuerySet of KVStoreNodes stores key values for nodes
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        p.kv.add(key="shop")
        p.kv.add(key="price")
        p.kv.add(key="date")

        self.assertEqual(
            3,
            p.kvstore.count()
        )

        p.kv.remove(key="shop")

        self.assertEqual(
            2,
            p.kvstore.count()
        )

    def test_basic_kvstorecomp_validations(self):
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        p.kvcomp.add(key=("date", "amount", "desc"))
        with self.assertRaises(KVCompKeyLengthMismatch):
            p.kvcomp.add(key=("date",))

    def test_kv_all_for_folder(self):
        """
        Get information about kv schema (kv key fields)
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        # no kv schema defined yet
        self.assertFalse(p.kv.all())
        p.kv.add(key="shop")
        self.assertTrue(p.kv.all())
        self.assertEqual(
            ['shop', ],
            [item.key for item in p.kv.all()]
        )

    def test_kvcomp_all_for_folder(self):
        """
        Get information about kvcomp
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        # no kvcomp defined yet
        self.assertFalse(p.kvcomp.all())
        p.kvcomp.add(key=("date", "amount", "desc"))
        self.assertTrue(p.kvcomp.all())

        # p.kvcomp returns a list of rows, each
        # column of the row can be accessed with [0], [1]...
        row1 = p.kvcomp.all()[0]
        self.assertEqual(
            row1[0].key,
            "date"
        )
        self.assertEqual(
            row1[1].key,
            "amount"
        )

    def test_basic_kvstorecomp_for_folder(self):
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        p.kvcomp.add(key=("date", "amount", "desc"))

        self.assertEqual(
            1,
            p.kvstorecomp.count()
        )

    def test_folders_kvstore_propagates_to_subfolders(self):
        """
        Folder's kvstore propagates to all its descendent folders,
        documents, pages
        """
        top = Folder.objects.create(
            title="top",
            user=self.user
        )
        top.save()
        sub = Folder.objects.create(
            title="sub",
            parent=top,
            user=self.user
        )
        sub.save()
        self.assertEqual(
            0,
            top.kvstore.count()
        )
        self.assertEqual(
            0,
            sub.kvstore.count()
        )
        top.kv.add(key="shop")
        self.assertEqual(
            1,
            top.kvstore.count()
        )
        # kvstore propagated from parent folder to descendents
        self.assertEqual(
            1,
            sub.kvstore.count()
        )
