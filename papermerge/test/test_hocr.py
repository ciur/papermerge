import tempfile
import json
import os
from pathlib import Path

from django.test import TestCase
from papermerge.core.lib.hocr import Hocr, OcrxWord, extract_size

BASE_DIR = Path(__file__).parent


class TestHocr(TestCase):
    def test_extract_words_from(self):
        hocr_file = os.path.join(
            BASE_DIR,
            "data",
            "page-1.hocr"
        )
        hocr = Hocr(hocr_file_path=hocr_file)

        try:
            json.dumps({
                'hocr': hocr.good_json_words(),
                'hocr_meta': hocr.get_meta()
            })
        except TypeError:
            self.assertTrue(
                False,
                "Unserializable result"
            )

    def test_extract_size_func(self):
        title = "image blah/blah; bbox 0 0 300 600; ppageno 0"
        width, height = extract_size(title)

        self.assertEqual(
            width,
            300
        )
        self.assertEqual(
            height,
            600
        )

    def test_extract_img_size(self):
        hocr_file = os.path.join(
            BASE_DIR,
            "data",
            "page-1.hocr"
        )
        hocr = Hocr(hocr_file_path=hocr_file)

        self.assertEqual(
            hocr.width,
            1240
        )

        self.assertEqual(
            hocr.height,
            1754
        )

    def test_ocrx_bbox(self):
        word = OcrxWord(
            el_class="ocrx_word",
            el_id="word_1_218",
            title="bbox 102 448 120 457; x_wconf 38",
            text="Dder"
        )
        self.assertEqual(
            word.x1, 102
        )
        self.assertEqual(
            word.y1, 448
        )
        self.assertEqual(
            word.x2, 120
        )
        self.assertEqual(
            word.y2, 457
        )
        self.assertEqual(
            word.wconf,
            38
        )

    def test_empty_file_hocr(self):
        """
        If empty or invalid file is provided then
        json_good_words() and get_meta()
        will return empty list.
        """
        file = tempfile.NamedTemporaryFile(mode="r+t")
        hocr = Hocr(hocr_file_path=file.name)

        self.assertEqual(
            hocr.good_json_words(),
            []
        )
        meta = hocr.get_meta()
        self.assertEqual(
            meta,
            {
                'count_all': 0,
                'bad_words': [],
                'count_good': 0,
                'count_bad': 0,
                'count_non_empty': 0,
                'count_low_wconf': 0,
                'width': 0,
                'height': 0,
                'min_wconf': 30
            }
        )
        file.close()
