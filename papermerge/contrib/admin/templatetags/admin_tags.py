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
def boolean_icon(boolean_value, show_empty_on_false=False):

    icon_html = mark_safe("<i class='fa {} {}'></i>")

    if boolean_value:
        return format_html(
            icon_html,
            "fa-check",
            "text-success"
        )

    if show_empty_on_false:
        return ''

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
def tags_line(item):
    """
    item must have tags attribute (item.tags.all() iteratable)
    """
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
        for tag in item.tags.all()
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


@register.simple_tag(takes_context=True)
def localized_datetime(context, datetime_instance):
    user = context['request'].user

    if user:
        date_fmt = user.preferences['localization__date_format']
        time_fmt = user.preferences['localization__time_format']
        # include seconds as well
        fmt = f"{date_fmt} {time_fmt}:%S"
        ret_str = datetime_instance.strftime(fmt)

        return ret_str


@register.simple_tag(takes_context=True)
def select_if_current_version(context, version, forloop_first):
    """
    Decide if current select option should be selected or no.
    This template is called within a for loop of document versions.

    This simple tag is used in info widget of the document (if document
    has more then one version).
    If document has more then one version, a select tag will be used so that
    user can select which document version will be displayed in documet viewer.

    The fact that version X is currently displayed to the user is determined by
    URL GET parameter http://.../?version=X.
    Thus, if URL parameter version == 'X' and simple tag argument
    ``version`` == 'X' then this current option must be selected.
    In case when URL parameter version is not present at all - the last
    version will be selected. We are iterating along with first element
    if ``forloop_first`` argument is True.
    """
    request = context['request']
    param_version = request.GET.get('version', None)

    if param_version is None:
        if forloop_first:
            return 'selected'

    # here param_version is not None
    str_version = str(version)

    if str_version == param_version:
        return 'selected'

    return ''


def is_latest_version(version, versions):
    if version is None:
        return True

    version = int(version)
    if versions:
        if version == int(versions[-1]):
            return True

    return False


@register.simple_tag(takes_context=True)
def thumb_arrow_up(context):
    """
    User can change page order (move page up) only is currently
    latest version of the document is displayed
    """
    has_perm_write = context['has_perm_write']
    request = context['request']
    versions = context['versions']
    version = request.GET.get('version', None)

    ret = mark_safe(
        "<div class='arrow-up-control'>"
        "<a href='#'><i class='fa fa-arrow-circle-up'></i></a>"
        "</div>"
    )

    if has_perm_write and is_latest_version(
        version, versions
    ):
        return ret

    return ''


@register.simple_tag(takes_context=True)
def thumb_arrow_down(context):
    """
    User can change page order (move page down) only is currently
    latest version of the document is displayed
    """
    has_perm_write = context['has_perm_write']
    request = context['request']
    versions = context['versions']
    version = request.GET.get('version', None)

    ret = mark_safe(
        "<div class='arrow-down-control'>"
        "<a href='#'><i class='fa fa-arrow-circle-down'></i></a>"
        "</div>"
    )

    if has_perm_write and is_latest_version(
        version, versions
    ):
        return ret

    return ''
