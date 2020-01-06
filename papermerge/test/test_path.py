from django.test import TestCase
from papermerge.core.lib.path import filter_by_extention


class TestFolder(TestCase):
    def test_filter_all_good(self):
        all_good = [
            'document_365-page-2.jpg',
            'document_365-page-3.jpg',
            'document_365-page-1.jpg'
        ]
        result = filter_by_extention(all_good)
        # nothing should be filtered, as by dafault all
        # extentions are supported
        self.assertEqual(
            result, all_good
        )

    def test_filter_out_invalid_bmp(self):
        files_list = [
            'document_365-page-2.jpg',
            'document_365-page-3.bmp',
            'document_365-page-1.bmp'
        ]
        result = filter_by_extention(files_list)
        self.assertEqual(
            result, ['document_365-page-2.jpg']
        )

    def test_filter_out_without_ext(self):
        files_list = [
            'document_365-page',
            'document_365-page',
            'document_365-page-1.bmp'
        ]
        result = filter_by_extention(files_list)
        # files without extentions will be fileted out
        self.assertEqual(
            result, []
        )
