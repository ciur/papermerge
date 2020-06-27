from django.template import Library
from papermerge.core.lib.lang import LANG_DICT


register = Library()


@register.inclusion_tag('admin/widgets/ocr_language_select.html')
def ocr_language_select(user):
    languages = []
    for key, value in LANG_DICT.items():

        lang = {}
        lang['tsr_code'] = key
        lang['human'] = value.capitalize()
        if user.preferences['ocr__OCR_Language'] == key:
            lang['selected'] = 'selected'
        else:
            lang['selected'] = ''

        languages.append(lang)

    return {'languages': languages}
