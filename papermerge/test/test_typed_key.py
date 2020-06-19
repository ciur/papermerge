from django.test import TestCase
from papermerge.core.models.kvstore import TypedKey


class TestTypedKey(TestCase):

    def test_typed_key_equality_operator(self):

        tkey1 = TypedKey(
            "Steuernummer",
            "numeric",
            "dd/ddd/ddd"
        )
        tkey2 = TypedKey(
            "Steuernummer",
            "numeric",
            "dd/ddd/ddd"
        )
        self.assertEqual(
            tkey1,
            tkey2
        )

    def test_type_key_equality_set(self):

        tkey1 = TypedKey(
            "Steuernummer",
            "numeric",
            "dd/ddd/ddd"
        )
        tkey2 = TypedKey(
            "date",
            "date",
            "dd/mm/YYYY"
        )
        tkey3 = TypedKey(
            "Steuernummer",
            "numeric",
            "dd/ddd/ddd"
        )
        tkey4 = TypedKey(
            "date",
            "date",
            "dd/mm/YYYY"
        )
        self.assertEqual(
            set([tkey1, tkey2]),
            set([tkey3, tkey4])
        )
        self.assertNotEqual(
            set([tkey1]),
            set([tkey4])
        )
