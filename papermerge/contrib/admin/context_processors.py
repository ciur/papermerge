from papermerge.core.models import Folder


def extras(request):

    try:
        inbox = Folder.objects.get(
            title__iexact="inbox"
        )
        count = inbox.get_children().count()
    except Folder.DoesNotExist:
        count = -1

    return {
        'inbox_count': count,
    }
