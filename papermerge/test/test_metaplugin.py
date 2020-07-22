from django.test import TestCase
from papermerge.core.metadata_plugins import get_plugin_by_module_name


class TestMetadataPlugin(TestCase):

    def test_basic(self):
        """
        Simple test, just to get basic idea on how to use
        meta-plugin API
        """
        plugin_klass = get_plugin_by_module_name(
            "papermerge.test.metaplugin"
        )

        self.assertTrue(
            plugin_klass,
            "Plugin not found"
        )

        hocr = "It works!"

        plugin = plugin_klass()

        result = plugin.extract(hocr)
        self.assertEqual(
            result['simple_keys']['label_key_1'],
            "value_1"
        )
