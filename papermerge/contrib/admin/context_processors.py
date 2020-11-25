
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
