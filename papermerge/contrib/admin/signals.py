from django.dispatch import receiver


from papermerge.core.models import Folder

from papermerge.core.signal_definitions import (
    folder_created,
    nodes_deleted,
    page_ocr
)
from papermerge.core.utils import node_tag
from papermerge.contrib.admin.models import LogEntry


@receiver(page_ocr)
def page_ocr_handler(sender, **kwargs):
    pass


@receiver(folder_created)
def folder_created_handler(sender, **kwargs):
    folder_id = kwargs.get('folder_id')
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')

    folder = Folder.objects.get(id=folder_id)

    folder_tag = node_tag(folder)

    msg = f"Node/Folder {folder_tag} created"

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )


@receiver(nodes_deleted)
def nodes_deleted_handler(sender, **kwargs):
    node_tags = kwargs.get('node_tags')
    user_id = kwargs.get('user_id')
    level = kwargs.get('level')

    msg = f"Node(s) {','.join(node_tags)} were deleted"

    LogEntry.objects.create(
        user_id=user_id,
        level=level,
        message=msg
    )
