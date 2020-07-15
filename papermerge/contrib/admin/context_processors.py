from papermerge.core.models import Folder


def extras(request):

    inbox = Folder.objects.get(
        title__iexact="inbox"
    )

    return {
        'inbox_count': inbox.get_children().count(),
    }
