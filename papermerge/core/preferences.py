from pytz import common_timezones

from django.conf import settings

from dynamic_preferences.preferences import Section as OrigSection
from dynamic_preferences.types import ChoicePreference
from dynamic_preferences.users.registries import user_preferences_registry

from .lib.lang import get_ocr_lang_choices, get_default_ocr_lang


def _get_timezone_choices():
    return list((tz, tz) for tz in common_timezones)


class Section(OrigSection):
    def __init__(
        self,
        name,
        verbose_name=None,
        help_text=None,
        icon_name=None
    ):
        super().__init__(
            name=name,
            verbose_name=verbose_name
        )
        self.help_text = help_text
        self.icon_name = icon_name


localization = Section(
    'localization',
    verbose_name="Localization",
    icon_name="globe-americas",
    help_text="Timezone, date and time formats"
)

ocr = Section(
    'ocr',
    verbose_name="Opical Character Recognition",
    icon_name="eye",
    help_text='Choose default OCR Language'
)


@user_preferences_registry.register
class TimezoneGlobal(ChoicePreference):
    help_text = """
    Timezone
"""
    section = localization
    name = "timezone"
    choices = _get_timezone_choices()
    # fallback value
    default = settings.TIME_ZONE


@user_preferences_registry.register
class OcrLanguage(ChoicePreference):
    help_text = """
    Language used for OCR processing.
"""
    section = ocr
    name = 'OCR_Language'
    choices = get_ocr_lang_choices()
    default = get_default_ocr_lang()


@user_preferences_registry.register
class LocalizationDate(ChoicePreference):
    help_text = """
    Date format
"""
    section = localization
    name = 'date_format'
    choices = (
        ('%Y-%m-%d', '2020-11-25'),
        ('%a %d %b, %Y', 'Wed 25 Nov, 2020'),
        ('%d %b, %Y', '25 Nov, 2020'),
        ('%m/%d/%Y', '11/25/2020'),
        ('%d/%m/%Y', '25/11/2020'),
        ('%d.%m.%y', '25.11.20'),
        ('%d.%m.%Y', '25.11.2020'),
    )
    default = '%Y-%m-%d'


@user_preferences_registry.register
class LocalizationTime(ChoicePreference):
    help_text = """
    Time format
"""
    section = localization
    name = 'time_format'
    choices = (
        ('%I:%M %p', '9:48 PM'),
        ('%H:%M', '21:48'),
    )
    default = '%H:%M'
