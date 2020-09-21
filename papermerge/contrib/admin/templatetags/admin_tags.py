from django.template import Library
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

from papermerge.core.lib.lang import LANG_DICT
from papermerge.contrib.admin.models import LogEntry


register = Library()


def url_for_folder(node):
    return f"/#{node.id}"


def url_for_document(node):
    return f"/#{node.id}"


def build_url_for_index(
    html_class_attr='',
    title=''
):
    url = reverse('admin:index')

    link = format_html(
        '<a href="{}" class="{}" alt="{}">'
        '{}</a>',
        url,
        html_class_attr,
        title,
        title
    )

    return link


def build_url_for_node(node, html_class_attr=''):

    if node.is_folder():
        url = url_for_folder(node)
    else:
        url = url_for_document(node)

    link = format_html(
        '<a href="{}" class="{}" data-id="{}" alt="{}">'
        '{}</a>',
        url,
        html_class_attr,
        node.id,
        node.title,
        node.title
    )

    return link


def build_tree_path(
    node,
    include_self=False,
    include_index=False,
    html_class_attr=''
):
    """
    Returns an html formated path of the Node.
    Example:
        Documents > Folder A > Folder B > Document C
    Where each node is an html anchor with href to the element.
    Node is instance of core.models.BaseTreeNode.
    include_index will add url to the index of boss page.
    """
    if node:
        ancestors = node.get_ancestors(include_self=include_self)
    else:
        ancestors = []

    titles = [
        build_url_for_node(item, html_class_attr=html_class_attr)
        for item in ancestors
    ]

    if include_index:
        titles.insert(
            0,
            build_url_for_index(html_class_attr=html_class_attr)
        )

    return mark_safe(' › '.join(titles))


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


@register.simple_tag()
def search_folder_path(node):
    return build_tree_path(
        node,
        include_self=True,
        include_index=True,
        html_class_attr="mx-1"
    )


@register.simple_tag()
def search_document_path(node):
    return build_tree_path(
        node,
        include_self=False,
        include_index=False,
        html_class_attr="mx-1"
    )


@register.simple_tag()
def tree_path(node):
    return build_tree_path(
        node,
        include_self=True,
        include_index=False,
        html_class_attr="mx-1"
    )


@register.simple_tag()
def tags_list(automate):
    return " ".join(
        [tag.name for tag in automate.tags.all()]        
    )


@register.simple_tag()
def search_tags_line(node):
    li = "<li class='tag' style='color:{}; background-color:{}'>{}</li>"
    li_items = [
        format_html(
            mark_safe(
                li
            ),
            tag.fg_color,
            tag.bg_color,
            tag.name
        )
        for tag in node.tags.all()
    ]
    result = format_html(
        mark_safe(''.join(li_items))
    )

    return result


@register.filter
def log_level(level_as_int):
    """
    logging.INFO -> _("Info")
    logging.DEBUG -> _("Debug")
    etc
    """

    for level in LogEntry.LEVELS:
        if level_as_int == level[0]:
            return level[1]

    return None
