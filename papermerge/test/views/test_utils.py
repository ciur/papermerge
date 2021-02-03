from django.test import TestCase

from papermerge.core.views.utils import (
    sanitize_kvstore_list,
    sanitize_kvstore
)


class TestCoreViewsUtils(TestCase):

    def test_sanitize_kvstore_correct_keys(self):
        input_dict = {
            'id': '1',
            'key': 'X',
            'value': 'Y',
            'kv_type': 'text',
            'kv_format': 'freeform',
            'kv_inherited': False
        }
        out_dict = sanitize_kvstore(input_dict)

        self.assertDictEqual(
            input_dict,
            out_dict
        )

    def test_sanitize_with_invalid_keys(self):
        """
        input dictionary contains two invalid keys
        """
        expected_dict = {
            'id': '1',
            'key': 'X',
            'value': 'Y',
            'kv_type': 'text',
            'kv_format': 'freeform',
            'kv_inherited': False
        }

        input_dict = {
            'id': '1',
            'key': 'X',
            'invalid_key_1': 2,  # will be filtered out
            'invalid_key_2': 4,  # will be filtered out
            'value': 'Y',
            'kv_type': 'text',
            'kv_format': 'freeform',
            'kv_inherited': False
        }

        out_dict = sanitize_kvstore(input_dict)

        self.assertDictEqual(
            expected_dict,
            out_dict
        )

    def test_sanitize_kvstore_list_basic(self):

        with self.assertRaises(ValueError):
            # expects a list as argument, will
            # raise ValueError exception otherwise
            sanitize_kvstore_list({'key': 'value'})

    def test_sanitize_kvstore_list_all_correct_keys(self):
        """
        input list of dictionaries contains exact list of allowed keys
        """
        input_dict_list = [
            {
                'id': '1',
                'key': 'X',
                'value': 'Y',
                'kv_type': 'text',
                'kv_format': 'freeform',
                'kv_inherited': False
            },
        ]
        out_dict_list = sanitize_kvstore_list(input_dict_list)

        self.assertDictEqual(
            input_dict_list[0],
            out_dict_list[0]
        )

        self.assertEqual(
            len(input_dict_list),
            len(out_dict_list)
        )

    def test_sanitize_kvstore_list_with_invalid_keys(self):
        """
        input list of dictionaries contains two invalid keys
        """
        expected_dict_list = [
            {
                'id': '1',
                'key': 'X',
                'value': 'Y',
                'kv_type': 'text',
                'kv_format': 'freeform',
                'kv_inherited': False
            },
        ]
        input_dict_list = [
            {
                'id': '1',
                'key': 'X',
                'invalid_key_1': 2,  # will be filtered out
                'invalid_key_2': 4,  # will be filtered out
                'value': 'Y',
                'kv_type': 'text',
                'kv_format': 'freeform',
                'kv_inherited': False
            },
        ]
        out_dict_list = sanitize_kvstore_list(input_dict_list)

        self.assertDictEqual(
            expected_dict_list[0],
            out_dict_list[0]
        )

        self.assertEqual(
            len(input_dict_list),
            len(expected_dict_list)
        )
