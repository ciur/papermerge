
import papermerge
from papermerge.core.models import Folder

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

    return {
        'inbox_count': count,
        'papermerge_version': papermerge.__version__
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
