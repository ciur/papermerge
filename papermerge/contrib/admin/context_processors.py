
import papermerge
from papermerge.core.models import (
    Folder,
    Tag
)
from papermerge.core.forms import AdvancedSearchForm


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
            'has_perm_change_user': False
        }

    change_user = request.user.has_perm(
        'core.change_user',
    )
    return {
        'has_perm_change_user': change_user
    }
