"""
A general meta plugin dummy
"""

class Dummy:

    SIMPLE_KEYS = [
        'label_key_1',
        'label_key_2',
    ]

    def extract(self, hocr):

        result = {
            'simple_keys': {
                'label_key_1': 'value_1',
                'label_key_2': 'value_2',
            },
            'comp_key': []
        }

        return result
