from pytz import common_timezones

from dynamic_preferences.preferences import Section as OrigSection
from dynamic_preferences.registries import global_preferences_registry
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


timezone = Section(
    'timezone',
    verbose_name="Timezone",
    icon_name="globe-americas",
    help_text="Timezone"
)

localization_datetime = Section(
    'datetime',
    verbose_name="Date and Time",
    icon_name="clock",
    help_text="Set here date and time formats"
)

ocr = Section(
    'ocr',
    verbose_name="Opical Character Recognition",
    icon_name="eye",
    help_text='Choose default OCR Language'
)


@global_preferences_registry.register
class TimezoneGlobal(ChoicePreference):
    help_text = """
    Timezone
"""
    section = timezone
    name = "timezone"
    choices = _get_timezone_choices()
    default = 'Europe/Berlin'


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
    section = localization_datetime
    name = 'date_format'
    choices = (
        ('1', '2020-11-25'),
        ('2', 'Wed 25 Nov, 2020'),
        ('3', '25 Nov, 2020'),
        ('4', '11/25/2020'),
        ('5', '25/11/2020'),
        ('6', '25.11.20'),
        ('7', '25.11.2020'),
    )
    default = '1'


@user_preferences_registry.register
class LocalizationTime(ChoicePreference):
    help_text = """
    Time format
"""
    section = localization_datetime
    name = 'time_format'
    choices = (
        ('1', '9:48 PM'),
        ('2', '21:48'),
    )
    default = '2'
