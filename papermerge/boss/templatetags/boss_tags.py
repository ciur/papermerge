# coding: utf-8

from __future__ import unicode_literals

import datetime
import warnings

from django.conf import settings
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import (display_for_field, display_for_value,
                                        lookup_field, quote)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template import Library
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from papermerge.core.lib.lang import LANG_DICT
from papermerge.core.models import Access

try:
    from django.urls import NoReverseMatch
except ImportError:  # Django < 1.10 pragma: no cover
    from django.core.urlresolvers import NoReverseMatch
try:
    from django.utils.deprecation import RemovedInDjango20Warning
except ImportError:
    RemovedInDjango20Warning = RuntimeWarning


MPTT_ADMIN_LEVEL_INDENT = getattr(settings, 'MPTT_ADMIN_LEVEL_INDENT', 10)

register = Library()


def remote_field(field):
    # function copied from mptt v0.9.0 mptt.compat module
    # in mptt v0.9.1 it was removed
    # very likely that code using it will need refactoring.
    # TODO: ^
    return field.remote_field if hasattr(field, 'remote_field') else getattr(field, 'rel', None)


@register.simple_tag()
def breadcrumbs_tree_path(node):
    return build_tree_path(
        node,
        include_self=True,
        include_index=True,
        html_class_attr="reverse"
    )


###
# Ripped from contrib.admin (1.10)
def _coerce_field_name(field_name, field_index):
    """
    Coerce a field_name (which may be a callable) to a string.
    """
    if callable(field_name):
        if field_name.__name__ == '<lambda>':
            return 'lambda' + str(field_index)
        else:
            return field_name.__name__
    return field_name


def get_empty_value_display(cl):
    if hasattr(cl.model_admin, 'get_empty_value_display'):
        return cl.model_admin.get_empty_value_display()
    else:
        # Django < 1.9
        from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        return EMPTY_CHANGELIST_VALUE


###
# Ripped from contrib.admin's (1.10) items_for_result tag.
# The only difference is we're indenting nodes according to their level.
def mptt_items_for_result(cl, result, form):
    """
    Generates the actual list of data.
    """
    # each key in the returned result is the name of the model's field as
    # follows:
    # * "action_checkbox"
    # * "title_with_class"
    yielded_result = {}

    def link_in_col(is_first, field_name, cl):
        if cl.list_display_links is None:
            return False
        if is_first and not cl.list_display_links:
            return True
        return field_name in cl.list_display_links

    first = True
    pk = cl.lookup_opts.pk.attname

    for field_index, field_name in enumerate(cl.list_display):
        # #### MPTT SUBSTITUTION START
        empty_value_display = get_empty_value_display(cl)
        # #### MPTT SUBSTITUTION END
        row_classes = [
            'field-%s' % _coerce_field_name(field_name, field_index)
        ]
        try:
            f, attr, value = lookup_field(field_name, result, cl.model_admin)
        except ObjectDoesNotExist:
            result_repr = empty_value_display
        else:
            empty_value_display = getattr(
                attr,
                'empty_value_display',
                empty_value_display
            )
            if f is None or f.auto_created:
                if field_name == 'action_checkbox':
                    row_classes = ['action-checkbox']
                allow_tags = getattr(attr, 'allow_tags', False)
                boolean = getattr(attr, 'boolean', False)
                # #### MPTT SUBSTITUTION START
                try:
                    # Changed in Django 1.9, now takes 3 arguments
                    result_repr = display_for_value(
                        value, empty_value_display, boolean)
                except TypeError:
                    result_repr = display_for_value(value, boolean)
                # #### MPTT SUBSTITUTION END
                if allow_tags:
                    warnings.warn(
                        "Deprecated allow_tags attribute used on field {}. "
                        "Use django.utils.safestring.format_html(), "
                        "format_html_join(), or mark_safe() instead.".format(
                            field_name
                        ),
                        RemovedInDjango20Warning
                    )
                    result_repr = mark_safe(result_repr)
                if isinstance(value, (datetime.date, datetime.time)):
                    row_classes.append('nowrap')
            else:
                # #### MPTT SUBSTITUTION START
                is_many_to_one = isinstance(
                    remote_field(f),
                    models.ManyToOneRel
                )
                if is_many_to_one:
                    # #### MPTT SUBSTITUTION END
                    field_val = getattr(result, f.name)
                    if field_val is None:
                        result_repr = empty_value_display
                    else:
                        result_repr = field_val
                else:
                    # #### MPTT SUBSTITUTION START
                    try:
                        result_repr = display_for_field(value, f)
                    except TypeError:
                        # Changed in Django 1.9, now takes 3 arguments
                        result_repr = display_for_field(
                            value, f, empty_value_display)
                    # #### MPTT SUBSTITUTION END
                if isinstance(
                    f,
                    (models.DateField, models.TimeField, models.ForeignKey)
                ):
                    row_classes.append('nowrap')
        if force_text(result_repr) == '':
            result_repr = mark_safe('&nbsp;')
        row_class = mark_safe(' class="%s"' % ' '.join(row_classes))

        # If list_display_links not defined,
        # add the link tag to the first field
        if link_in_col(first, field_name, cl):
            first = False

            # Display link to the result's change_view if the url exists, else
            # display just the result's representation.
            try:
                url = cl.url_for_result(result)
            except NoReverseMatch:
                link_or_text = result_repr
            else:
                url = add_preserved_filters(
                    {
                        'preserved_filters': cl.preserved_filters,
                        'opts': cl.opts
                    },
                    url,
                )
                # Convert the pk to something that can be used in Javascript.
                # Problem cases are long ints (23L) and non-ASCII strings.
                if cl.to_field:
                    attr = str(cl.to_field)
                else:
                    attr = pk
                value = result.serializable_value(attr)

            yielded_result[field_name] = {
                'row_class': row_class,
                'repr': result_repr,
            }
        else:
            # By default the fields come from ModelAdmin.list_editable,
            # but if we pull
            # the fields out of the form instead of list_editable custom admins
            # can provide fields on a per request basis
            if (form and field_name in form.fields and not (
                    field_name == cl.model._meta.pk.name and
                    form[cl.model._meta.pk.name].is_hidden)):
                bf = form[field_name]
                result_repr = mark_safe(force_text(bf.errors) + force_text(bf))

            yielded_result[field_name] = {
                'row_class': row_class,
                'repr': result_repr,
            }

    _, _, _id = lookup_field('id', result, cl.model_admin)
    yielded_result['id'] = _id
    # ctype = Document | Folder
    yielded_result['ctype'] = str(result.polymorphic_ctype)
    yielded_result['is_document'] = result.is_document()
    yielded_result['is_folder'] = result.is_folder()
    if (result.is_document()):
        yielded_result['text'] = result.get_real_instance().text
    yielded_result['title'] = str(result.title)

    yield yielded_result


def mptt_results(cl):
    if cl.formset:
        for res, form in zip(cl.result_list, cl.formset.forms):
            yield list(mptt_items_for_result(cl, res, form))
    else:
        for res in cl.result_list:
            yield list(mptt_items_for_result(cl, res, None))


def url_for_folder(node):
    return reverse(
        'admin:core_basetreenode_changelist_obj',
        args=(quote(node.id),),
        current_app='boss'
    )


def url_for_document(node):
    return reverse(
        'admin:core_basetreenode_change',
        args=(quote(node.id),),
        current_app='boss'
    )


def build_url_for_index(
    html_class_attr='',
    title='Documents'
):
    url = reverse(
        'admin:core_basetreenode_changelist',
        current_app='boss'
    )

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


def get_icon_html(node):
    result = ''
    if node.is_folder():
        result = "<i class='yellow-folder margin-y-sm'></i>"
    else:
        #if len(node.text) > 0:
        #    result = "<i class='file margin-y-sm'></i>"
        #else:
        result = "<i class='file-empty margin-y-sm'></i>"

    return mark_safe(result)


def get_text(node):

    if node.is_document():
        return node.text

    return ''


def mptt_search_results(cl, user):
    results = []
    for node in cl.result_list:
        if user.has_perm(Access.PERM_READ, node):
            results.append({
                'icon': get_icon_html(node),
                'dir_path': build_tree_path(node),
                'title': build_url_for_node(node),
                'text': get_text(node),
                'model_ctype': node.polymorphic_ctype_id,
                'is_folder': node.is_folder(),
                'is_document': node.is_document()
            })

    return results


def result_page_headers(cl):

    result = []
    instance = cl.queryset.first()

    if not instance:
        return []

    result.append({'text': 'title'})

    for kvstore in instance.kv.all():
        result.append(
            {'text': kvstore.key}
        )

    result.append({'text': 'created_at'})

    return result


def result_page_items(cl):
    result = []

    nodes = cl.queryset.all()

    for node in nodes:
        _dict = {
            'id': node.id,
            'title': node.title,
            'created_at': node.created_at
        }
        if node.is_document():
            page = node.pages.first()
            kvstore = [
                {'key': kv.key, 'value': kv.value} for kv in page.kv.all()
            ]
            _dict['kvstore'] = kvstore
        else:
            kvstore = [
                {'key': kv.key, 'value': kv.value} for kv in node.kv.all()
            ]
            _dict['kvstore'] = kvstore

        result.append(_dict)

    return result


def boss_result(cl):
    return {
        'cl': cl,
        'result_headers': result_page_headers(cl),
        'results': list(mptt_results(cl))
    }


@register.inclusion_tag('boss/mptt_change_list_results_grid.html')
def boss_result_grid(cl):
    """
    Displays the headers and data list together
    """
    return boss_result(cl)


@register.inclusion_tag('boss/mptt_change_list_results_list.html')
def boss_result_list(cl):
    """
    Displays the headers and data list together
    """
    return {
        'cl': cl,
        'result_headers': result_page_headers(cl),
        'results': result_page_items(cl)
    }


@register.inclusion_tag(
    'boss/mptt_change_list_search_results.html',
    takes_context=True
)
def boss_search_results(context, cl, user):
    """
    Displays search results as a list using search specific view
    """
    context['cl'] = cl
    context['results'] = mptt_search_results(cl, user)
    
    return context


@register.simple_tag
def login_tag():

    title = gettext('Sign In here')
    link = reverse('login')

    return format_html(
        '<a href="{}">{}</a>',
        link,
        title
    )


@register.simple_tag
def register_tag():
    title = gettext('please register')
    link = reverse('register')

    return format_html(
        '<a href="{}">{}</a>',
        link,
        title
    )


@register.inclusion_tag('boss/ocr_language_select.html')
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
