from papermerge.core.models import Folder


def extras(request):

    if request.user.is_anonymous:
        return {
            'inbox_count': -1
        }

    try:
        inbox = Folder.objects.get(
            title__iexact="inbox",
            user=request.user
        )
        count = inbox.get_children().count()
    except Folder.DoesNotExist:
        count = -1

    return {
        'inbox_count': count,
    }
