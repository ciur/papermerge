from pathlib import Path

from django.test import TestCase
from papermerge.core.models import Document, Folder
from papermerge.core.models.kvstore import MONEY, TEXT, KVCompKeyLengthMismatch
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

    def test_folders_kvstore_propagates_add_to_subfolders(self):
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
        doc = Document.objects.create_document(
            title="document_in_sub",
            file_name="document_sub.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=sub.id,
            page_count=5,
        )
        doc.save()
        self.assertEqual(
            0,
            top.kvstore.count()
        )
        self.assertEqual(
            0,
            sub.kvstore.count()
        )
        self.assertEqual(
            0,
            doc.kvstore.count()
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
        # kvstore propagated from ancestor folder to doc
        self.assertEqual(
            1,
            doc.kvstore.count()
        )

    def test_update_duplicates_1_kv(self):
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        self.assertEqual(0, p.kv.count())
        p.kv.update(
            [{'key': "shop"}, {'key': "shop"}]
        )
        # duplicates will be silently discarded
        self.assertEqual(1, p.kv.count())
        self.assertEqual(
            set(p.kv.keys()), set(["shop"])
        )

    def test_update_duplicates_2_kv(self):
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        self.assertEqual(0, p.kv.count())
        p.kv.update(
            [{'key': "shop"}, {'key': "total"}]
        )
        self.assertEqual(2, p.kv.count())
        p.kv.update(
            [{'key': "shop"}, {'key': "total"}]
        )
        # update with already existing keys - will be silently discarded
        self.assertEqual(2, p.kv.count())
        self.assertEqual(
            set(p.kv.keys()), set(["shop", "total"])
        )

    def test_update_existing_kv_name(self):
        """
        1. User adds 2 simple keys for folder titled "P":
            * shop
            * total
        2. User opens again metadata menu, he sees:
            * shop
            * total
        3. He renames total -> total_price
        Result must be that an existing kv instance will be updated.
        """
        p = Folder.objects.create(
            title="P",
            user=self.user
        )
        self.assertEqual(0, p.kv.count())
        p.kv.update(
            [
                {'key': 'shop', 'kv_type': TEXT, 'kv_format': ''},
                {'key': 'total', 'kv_type': MONEY, 'kv_format': 'dd,cc'}
            ]
        )
        self.assertEqual(2, p.kv.count())
        # get ID's of newly created KVStoreNode instances
        _kv_list_of_dicts = [
            {
                'key': item.key,
                'id': item.id,
                'kv_type': item.kv_type,
                'kv_format': item.kv_format
            } for item in p.kv.all()
        ]
        # find key titled 'total', and rename it to 'total_price'
        for obj_with_total_key in _kv_list_of_dicts:
            if obj_with_total_key['key'] == 'total':
                break
        else:
            obj_with_total_key = None

        if obj_with_total_key:
            obj_with_total_key['key'] = 'total_price'

        # Will update existing KVStoreNode (identified by 'id').
        # Will change it's key from 'total' -> 'total_price'
        p.kv.update(_kv_list_of_dicts)
        # p.kv.count should not change
        self.assertEqual(2, p.kv.count())
        # set of kv keys will differ now
        self.assertEqual(
            set(p.kv.keys()), set(["shop", "total_price"])
        )

    def test_updating_multiple_times(self):
        """
        updating multiple times (with same keys, or edited keys), does not
        create duplicate metadata on descending nodes.

        User creates 2 folders:
            * top
              |--sub

        When he updates multiple times 'top' folder metadata, it does not
        create duplicates in descending folder 'sub'

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
        top.kv.update(
            [{'key': 'shop'}, {'key': 'total'}]
        )
        top.kv.update(
            [{'key': 'shop'}, {'key': 'total'}]
        )
        self.assertEqual(2, top.kv.count())
        # there are not duplicates in descendents' metadata.
        self.assertEqual(2, sub.kv.count())
        top.kv.update(
            [{'key': 'shop'}, {'key': 'total'}]
        )
        self.assertEqual(2, sub.kv.count())
        self.assertEqual(
            set(
                sub.kv.keys()
            ),
            set(
                top.kv.keys()
            )
        )

    def test_folders_kvstore_propagates_delete_to_subfolders(self):
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
        top.kv.update(
            [{'key': 'shop'}, {'key': 'total'}]
        )
        self.assertEqual(2, top.kv.count())
        # there are not duplicates in descendents' metadata.
        self.assertEqual(2, sub.kv.count())

        # user deletes key 'total' on the top folder
        top.kv.update(
            [{'key': 'shop'}]
        )
        # subfolder "sub" will will have now only one kv instance
        self.assertEqual(1, sub.kv.count())
        # which is same as for its parent
        self.assertEqual(
            set(
                sub.kv.keys()
            ),
            set(
                top.kv.keys()
            )
        )
        # which is 'shop'
        self.assertEqual(
            set(
                sub.kv.keys()
            ),
            set(
                ["shop"]
            )
        )

    def test_folders_kvstore_propagates_update_to_subfolders(self):
        """
        This case is when descendent folders exists during metadata creation.
        i.e. creation order is this:
            1. top folder
            2. sub folder
            3. metadata on top folder
            4  metadata is inherited from top to already existing descendents.
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
        self.assertEqual(2, top.kv.count())
        # there are not duplicates in descendents' metadata.
        self.assertEqual(2, sub.kv.count())

        # user updates key shop to shop2 on the top folder
        shop_kv = next(
            filter(lambda x: x.key == 'shop', top.kv.all())
        )
        top.kv.update(
            [
                {
                    'key': 'shop2',
                    'id': shop_kv.id,
                    'kv_type': TEXT,
                    'kv_format': ''
                },
                {
                    'key': 'total',
                    'kv_type': MONEY,
                    'kv_format': 'dd,cc'
                },  # total key is unchanged
            ]
        )
        self.assertEqual(
            set(
                top.kv.keys()
            ),
            set(
                ["shop2", "total"]
            )
        )
        self.assertEqual(2, sub.kv.count())
        # which is same as for its parent
        self.assertEqual(
            set(
                sub.kv.keys()
            ),
            set(
                top.kv.keys()
            )
        )
        self.assertEqual(
            set(
                sub.kv.keys()
            ),
            set(
                ["shop2", "total"]
            )
        )

    def test_folders_kvstore_propagates_update_to_subfolders_2(self):
        """
        This case is when descendent folders DO NOT exists during
        metadata creation.
        i.e. creation order is this:
            1. top folder
            2. metadata on top folder
            3. Sub folder
            4. Metadata must be inherited by subfolder from top folder.
        """
        top = Folder.objects.create(
            title="top",
            user=self.user
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
        self.assertEqual(2, top.kv.count())
        # When subfolder is created - parent folder ALREADY has metadata.
        sub = Folder.objects.create(
            title="sub",
            parent=top,
            user=self.user
        )
        sub.save()
        # there are not duplicates in descendents' metadata.
        self.assertEqual(2, sub.kv.count())

        self.assertEqual(
            set(
                sub.kv.keys()
            ),
            set(
                ["shop", "total"]
            )
        )
