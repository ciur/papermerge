from django.conf import settings

"""
Tesseract uses ISO-639-2/T for language names
Postgres uses different way to name its languages.
LANG_DICT maps those two worlds.
"""
# key is ISO-639-2/T as per:
# https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
# value is language dictionary as as per
# psql> \dFd (which lists installed dictionaries)

LANG_DICT = settings.PAPERMERGE_OCR_LANGUAGES


def get_default_ocr_lang():

    return settings.PAPERMERGE_OCR_DEFAULT_LANGUAGE


def get_ocr_lang_choices(capitalize=True):
    """
    returns a list of tuples as required by
    Django's choices ((key, value),(key, value), ...)
    """

    return [
        (key, value.capitalize())
        for key, value in LANG_DICT.items()
    ]
