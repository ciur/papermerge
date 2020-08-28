from django.urls import reverse
from django.dispatch import receiver
from django.utils.html import format_html

from papermerge.core.models import Folder
from papermerge.core.signal_definitions import folder_created
from papermerge.contrib.admin.models import LogEntry


@receiver(folder_created)
def folder_created_handler(sender, **kwargs):
    folder_id = kwargs.get('folder_id')
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')

    folder = Folder.objects.get(id=folder_id)

    folder_url = reverse("core:node", args=(folder_id,))
    folder_tag = format_html(
        "<a href='{}'>{}</a>",
        folder_url,
        folder.title
    )

    msg = f"Folder {folder_tag} created"

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )
