from dynamic_preferences.types import (
    IntegerPreference,
    ChoicePreference
)

from dynamic_preferences.preferences import Section
from dynamic_preferences.users.registries import user_preferences_registry
from dynamic_preferences.registries import global_preferences_registry

from briolette import lang_human_name

ocr = Section('ocr')
system_settings = Section('system_settings')
user_views = Section('views')


@global_preferences_registry.register
class UserStorageSize(IntegerPreference):
    help_text = """
    Storage size allocated for users. It is expressed in MB.
    """
    section = system_settings
    name = "user_storage_size"
    default = 128 * 1024


@user_preferences_registry.register
class DocumentsView(ChoicePreference):
    help_text = """
    Display documents as grid or list view
    """
    section = user_views
    name = "documents_view"
    choices = (
        ('grid', 'Grid'),
        ('list', 'List')
    )
    default = 'grid'


@user_preferences_registry.register
class OcrLanguage(ChoicePreference):
        help_text = """
        Language used for OCR processing.
    """
        section = ocr
        name = 'OCR_Language'
        choices = (
            ('deu', lang_human_name('deu')),
            ('eng', lang_human_name('eng')),
        )
        default = 'deu'
