from django.db import models


class LanguageMap(models.Model):
    """
    Data table which maps Tesseract language code (tsr_code)
    (as specified from command line argument -l <lang>) to
    postgresql language catalog (pg_catalog column).
    Examples:
        tst_code       pg_catalog          pg_short
          deu       pg_catalog.german        german
          eng       pg_catalog.english       english
          spa       pg_catalog.spanish       spanish
          rus       pg_catalog.russian       russian
          ron       pg_catalog.romanian      romanian

    Tesseract uses ISO 639-2/T or ISO 639-2/B name for language codes.
    Here is full list:
        https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

    Postgres text search configurations are listed with

        psql> \dF  # noqa

    See papermerge.code.lib.lang.LANG_DICT
    """
    tsr_code = models.CharField(
        max_length=16,
        blank=False,
        null=False,
        unique=True
    )
    pg_catalog = models.CharField(
        max_length=64,
        blank=False,
        null=False
    )
    pg_short = models.CharField(
        max_length=64,
        blank=False,
        null=False
    )
