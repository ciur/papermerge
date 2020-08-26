import lxml
import lxml.html
import re
import logging


logger = logging.getLogger(__name__)


def extract_size(title):
    box_re = re.compile(
        '.*; bbox (?P<x1>\d+) (?P<y1>\d+) (?P<x2>\d+) (?P<y2>\d+);.*'
    )
    width = None
    height = None
    matched_obj = re.match(box_re, title)
    if matched_obj:
        width = int(matched_obj['x2'])
        height = int(matched_obj['y2'])

    return width, height


class OcrxWord:
    def __init__(self, el_class, el_id, title, text=''):
        """
        span_elem is item from array returnd by lxml.html's xpath
        method
        """
        self.el_class = el_class
        self.el_id = el_id
        self.title = title
        self.text = text
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.wconf = 0
        self.build_bbox_attrs(self.title)

    def build_bbox_attrs(self, title):
        """
        build x1, x2, y1, y2 and wconf attribues from title string.

        Example of title strings:

        'bbox 102 448 120 457; x_wconf 38'
        """
        box_re = re.compile(
            'bbox (?P<x1>\d+) (?P<y1>\d+) (?P<x2>\d+) (?P<y2>\d+); x_wconf (?P<wconf>\d+)'
        )
        matched_obj = re.match(box_re, title)
        if matched_obj:
            self.x1 = int(matched_obj['x1'])
            self.y1 = int(matched_obj['y1'])
            self.x2 = int(matched_obj['x2'])
            self.y2 = int(matched_obj['y2'])
            self.wconf = int(matched_obj['wconf'])
        else:
            logger.info(
                f"Word title mismatch.title={self.title}, el_id={self.el_id}."
            )

    def to_hash(self):
        """
        returns hash structure from OcrxWord attributes.
        """
        return {
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'wconf': self.wconf,
            'id': self.el_id,
            'title': self.title,
            'text': self.text,
            'class': self.el_class
        }


class Hocr:
    """Manages ocrx words from hocr file.
    """

    def __init__(self, hocr_file_path, min_wconf=30):
        self.hocr_file_path = hocr_file_path
        self.ocrx_words = []
        self.min_wconf = min_wconf
        self._width = 0
        self._height = 0
        try:
            self.extract()
        except lxml.etree.ParserError:
            logger.warning(
                f"Hocr file {hocr_file_path}"
                " is either empty of not of HOCR format"
            )

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def extract(self):
        html = None

        with open(self.hocr_file_path, "rb") as f:
            text = f.read()
            html = lxml.html.fromstring(text)

        page = html.xpath("//div[@class='ocr_page']")
        if len(page) > 0:
            self._width, self._height = extract_size(
                page[0].attrib['title']
            )

        for span in html.xpath("//span[@class='ocrx_word']"):
            elem = OcrxWord(
                el_class=span.attrib['class'],
                el_id=span.attrib['id'],
                title=span.attrib['title'],
                text=span.text
            )
            self.ocrx_words.append(elem)

        return self.ocrx_words

    def good_json_words(self):
        """Return only:
            * ocrx words with non empty text
            * ocrx words with w_conf > min_w_conf
        """
        meta = self._filter_words()
        return meta['good_words']

    def _filter_words(self):
        meta = {}
        meta['count_all'] = len(self.ocrx_words)
        meta['bad_words'] = []
        meta['good_words'] = []
        meta['count_non_empty'] = 0
        meta['count_low_wconf'] = 0
        meta['width'] = self.width
        meta['height'] = self.height
        meta['min_wconf'] = self.min_wconf

        for word in self.ocrx_words:
            bad_word = False
            if word.text and len(word.text) == 0:
                bad_word = True
                meta['bad_words'].append(word.to_hash())
                meta['count_non_empty'] += 1

            if word.wconf < self.min_wconf:
                bad_word = True
                meta['bad_words'].append(word.to_hash())
                meta['count_low_wconf'] += 1

            if not bad_word:
                meta['good_words'].append(word.to_hash())

        meta['count_bad'] = len(meta['bad_words'])
        meta['count_good'] = len(meta['good_words'])

        return meta

    def get_meta(self):
        meta = self._filter_words()

        return {
            'width': meta['width'],
            'height': meta['height'],
            'count_all': meta['count_all'],
            'count_bad': meta['count_bad'],
            'count_good': meta['count_good'],
            'count_non_empty': meta['count_non_empty'],
            'count_low_wconf': meta['count_low_wconf'],
            'bad_words': meta['bad_words'],
            'min_wconf': meta['min_wconf']
        }
