
import papermerge
from papermerge.core.models import (
    Folder,
    Tag
)
from .forms import AdvancedSearchForm
from .registries import user_menu_registry


def user_menu(request):
    values = list(user_menu_registry.values())

    return {
        'user_menu': values
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
        'papermerge_version': papermerge.__version__,
        'form': form,
        'alltags': alltags
    }


def user_perms(request):
    if request.user.is_anonymous:
        return {
            'has_perm_change_user': False,
            'has_perm_view_users': False,
            'has_perm_view_groups': False,
            'has_perm_view_automates': False,
            'has_perm_view_tags': False,
            'has_perm_view_logs': False,
        }

    change_user = request.user.has_perm(
        'core.change_user',
    )

    if request.user.is_superuser:
        return {
            'has_perm_change_user': change_user,
            'has_perm_view_users': True,
            'has_perm_view_groups': True,
            'has_perm_view_automates': True,
            'has_perm_view_tags': True,
            'has_perm_view_logs': True,
        }

    view_users = request.user.has_perm('admin.view_user')
    view_groups = request.user.has_perm('admin.view_group')
    view_automates = request.user.has_perm('admin.view_automate')
    view_tags = request.user.has_perm('admin.view_tag')
    view_logs = request.user.has_perm('admin.view_log')

    return {
        'has_perm_change_user': change_user,
        'has_perm_view_users': view_users,
        'has_perm_view_groups': view_groups,
        'has_perm_view_automates': view_automates,
        'has_perm_view_tags': view_tags,
        'has_perm_view_logs': view_logs,
    }
