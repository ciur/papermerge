import lxml.html


def parse_bbox_title(bbox_title):
    """Gets a string like
    input: 'bbox 23 344 45 66; x_wconf 88'
    output a hash:  {x1: 23, y1: 344, x2: 45, y2: 66, wconf: 88}

    Look here: http://kba.cloud/hocr-spec/1.2/
    for bbox and x_wconf properties.
    """
    pass


def extract_words_from(hocr_file):
    html = None
    result = []

    with open(hocr_file, "rb") as f:
        text = f.read()
        html = lxml.html.fromstring(text)

    for span in html.xpath("//span[@class='ocrx_word']"):
        elem = {}
        elem['class'] = span.attrib['class']
        elem['id'] = span.attrib['id']
        bbox = parse_bbox_title(span.attrib['title'])
        elem['title'] = span.attrib['title']
        elem['text'] = span.text
        elem['x1'] = bbox['x1']
        elem['x2'] = bbox['x1']
        elem['y1'] = bbox['y1']
        elem['y2'] = bbox['y2']
        elem['wconf'] = bbox['wconf']

        result.append(elem)

    return result
