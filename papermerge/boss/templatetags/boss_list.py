from django.template import Library
from django.contrib.admin.views.main import (
    SEARCH_VAR,
)
from django.contrib.admin.templatetags import admin_list

register = Library()


@register.inclusion_tag('admin/search_form.html')
def search_form(cl):
    """
    Display a search form for searching the list.
    """
    # this line was added to admin_list.search_form template tag
    # without it, viewing dashboard with empty search fails
    # (because search box was moved to header instead of changelist view)
    if not hasattr(cl, 'result_count'):
        return {
            'cl': {'query': '', 'search_fields': True},
            'search_var': SEARCH_VAR
        }

    return {
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR
    }


@register.inclusion_tag("boss/task/change_list_results.html")
def task_result_list(cl):
    """
    Display the headers and data list together.
    """
    return admin_list.result_list(cl)


@register.inclusion_tag("boss/group/change_list_results.html")
def group_result_list(cl):
    """
    Display the headers and data list together.
    """
    return admin_list.result_list(cl)


@register.inclusion_tag("boss/user/change_list_results.html")
def user_result_list(cl):
    """
    Display the headers and data list together.
    """
    return admin_list.result_list(cl)


@register.inclusion_tag(
    "boss/dynamic_preferences_users/change_list_results.html"
)
def preferences_result_list(cl):
    """
    Display the headers and data list together.
    """
    return admin_list.result_list(cl)
