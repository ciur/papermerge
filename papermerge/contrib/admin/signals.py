from django.urls import reverse
from django.dispatch import receiver
from django.utils.html import format_html

from papermerge.core.models import (
    Folder,
    BaseTreeNode
)
from papermerge.core.signal_definitions import (
    folder_created,
    nodes_deleted
)
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


@receiver(nodes_deleted)
def nodes_deleted_handler(sender, **kwargs):
    node_ids = kwargs.get('node_ids')
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')
    nodes = BaseTreeNode.objects.filter(id__in=node_ids)
    node_tags = []

    for node in nodes:
        node_url = reverse("core:node", args=(node.id, ))
        node_tag = format_html(
            "<a href='{}'>{}</a>",
            node_url,
            node.title
        )
        node_tags.append(
            node_tag
        )

    msg = f"Nodes {','.join(node_tags)} were deleted."

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )
