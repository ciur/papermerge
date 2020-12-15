from django.urls import reverse
from papermerge.core import __version__ as PAPERMERGE_VERSION
from papermerge.core.models import (
    Folder,
    Tag
)
from .forms import AdvancedSearchForm
from .registries import (
    user_menu_registry,
    navigation
)

ROLE_DEPENDENT_SIDEBAR_MENU = [
    {
        'required_perm': 'core.view_automate',
        'url': reverse('admin:automates'),
        'title': 'Automates',
        'css_icon_class': 'fa-robot',
        'activate_on': 'automates, automate-add, automate-update'
    },
    {
        'required_perm': None,
        'url': reverse('admin:tags'),
        'title': 'Tags',
        'css_icon_class': 'fa-tag',
        'activate_on': 'tags, tag-add, tag-update'
    },
    {
        'required_perm': None,
        'url': reverse('admin:logs'),
        'title': 'Logs',
        'css_icon_class': 'fa-lightbulb',
        'activate_on': 'logs, log-update'
    },
    {
        'required_perm': 'auth.view_group',
        'url': reverse('admin:groups'),
        'title': 'Groups',
        'css_icon_class': 'fa-users',
        'activate_on': 'groups, group-add, group-update'
    },
    {
        'required_perm': 'core.view_user',
        'url': reverse('admin:users'),
        'title': 'Users',
        'css_icon_class': 'fa-user-friends',
        'activate_on': 'users, user-add, user-update'
    },
    {
        'required_perm': 'core.view_role',
        'url': reverse('admin:roles'),
        'title': 'Roles',
        'css_icon_class': 'fa-user',
        'activate_on': 'roles, role-add, role-update'
    },
]


def sidebar_menu(request):
    """
    Builds sidebar menu depending on user role/permissions

    Sidebar menu is applicable only for authenticated users.
    """
    menu = []

    # menu item has following keys

    # 1. url
    # 2. title
    # 3. css_icon_class
    # 4. activate_on
    if request.user.is_anonymous:
        # main sidebar menu is applicable only for authenticated users
        return {}

    for menu_item in ROLE_DEPENDENT_SIDEBAR_MENU:
        req_perm = menu_item['required_perm']

        if not req_perm:
            menu.append(menu_item)

        if request.user.has_perm(req_perm):
            menu.append(menu_item)

    """
    lte_menu option determines the state of left menu of admin lte3
    (collapsed/expanded). It is used to decide which css class to set
    on <body> element (in admin/base.html).
    Why? Because with client side only solution, the user can see
    for fraction of second other state
    (during refresh -> collapse state -> ~ 0.2 sec -> expanded state)
    """

    return {
        'sidebar_menu': menu,
        'lte_menu': request.COOKIES.get('lte-menu', None)
    }


def user_menu(request):
    values = list(user_menu_registry.values())

    return {
        'user_menu': values
    }


def leftside_navigation(request):

    values = list(navigation.values())

    return {
        'leftside_navigation': values
    }


def extras(request):

    if request.user.is_anonymous:
        return {
            'inbox_count': -1
        }

    try:
        inbox = Folder.objects.get(
            title=Folder.INBOX_NAME,
            user=request.user
        )
        count = inbox.get_children().count()
    except Folder.DoesNotExist:
        count = -1

    pinned_tags = Tag.objects.filter(
        pinned=True,
        user=request.user
    )
    alltags = Tag.objects.filter(
        user=request.user
    )
    form = AdvancedSearchForm(user=request.user)

    return {
        'inbox_count': count,
        'pinned_tags': pinned_tags,
        'papermerge_version': PAPERMERGE_VERSION,
        'search_form': form,
        'alltags': alltags
    }


def user_perms(request):
    if request.user.is_anonymous:
        return {
            'has_perm_change_user': False
        }

    change_user = request.user.has_perm(
        'core.change_user',
    )
    return {
        'has_perm_change_user': change_user
    }
