from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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


@register.simple_tag(takes_context=True)
def activate_on(context, names):
    """
    names is a string of words separated by comma.
    Example:
        'group, groups'
        'users, user'

    Maybe a single word as well (without comma):
        'user'
    """
    cleaned_names = [
        name.strip() for name in names.split(',')
    ]
    if context['request'].resolver_match.url_name in cleaned_names:
        return 'active'

    return ''


@register.simple_tag
def boolean_icon(boolean_value):

    icon_html = mark_safe("<i class='fa {} {}'></i>")

    if boolean_value:
        return format_html(
            icon_html,
            "fa-check",
            "text-success"
        )

    return format_html(
        icon_html,
        "fa-times",
        "text-danger"
    )
