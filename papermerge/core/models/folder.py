from django.db import models
from django.utils.translation import ugettext_lazy as _

from polymorphic_tree.managers import (
    PolymorphicMPTTModelManager,
    PolymorphicMPTTQuerySet
)

from papermerge.core.models.diff import Diff
from papermerge.core.models.kvstore import (
    KVCompNode,
    KVNode,
    KVStoreNode,
    get_currency_formats,
    get_date_formats,
    get_kv_types,
    get_numeric_formats
)
from papermerge.core.models.node import (
    BaseTreeNode,
    RELATED_NAME_FMT,
    RELATED_QUERY_NAME_FMT
)
from papermerge.search import index


class FolderManager(PolymorphicMPTTModelManager):
    pass


class FolderQuerySet(PolymorphicMPTTQuerySet):

    def delete(self, *args, **kwargs):
        for node in self:
            descendants = node.get_descendants()

            if descendants.count() > 0:
                descendants.delete(*args, **kwargs)
            # At this point all descendants were deleted.
            # Self delete :)
            try:
                node.delete(*args, **kwargs)
            except BaseTreeNode.DoesNotExist:
                # this node was deleted by earlier recursive call
                # it is ok, just skip
                pass


CustomFolderManager = FolderManager.from_queryset(FolderQuerySet)

class Folder(BaseTreeNode, index.Indexed):

    # special folders' name always starts with a DOT (. character)
    INBOX_NAME = ".inbox"

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

    objects = CustomFolderManager()

    def delete(self, *args, **kwargs):
        descendants = self.basetreenode_ptr.get_descendants()

        if descendants.count() > 0:
            for node in descendants:
                try:
                    node.delete(*args, **kwargs)
                except BaseTreeNode.DoesNotExist:
                    pass
        # At this point all descendants were deleted.
        # Self delete :)
        try:
            super().delete(*args, **kwargs)
        except BaseTreeNode.DoesNotExist:
            # this node was deleted by earlier recursive call
            # it is ok, just skip
            pass

    def to_dict(self):
        item = {}

        item['id'] = self.id
        item['title'] = self.title
        item['created_at'] = self.human_created_at
        item['updated_at'] = self.human_updated_at
        item['timestamp'] = self.created_at.timestamp()

        if self.parent:
            item['parent_id'] = self.parent.id
        else:
            item['parent_id'] = ''
        item['ctype'] = 'folder'

        tags = []
        for tag in self.tags.all():
            tags.append(tag.to_dict())
        item['tags'] = tags

        kvstore = []
        for kv in self.kv.all():
            kvstore.append(kv.to_dict())

        item['metadata'] = {}
        item['metadata']['kvstore'] = kvstore
        item['metadata']['currency_formats'] = get_currency_formats()
        item['metadata']['date_formats'] = get_date_formats()
        item['metadata']['numeric_formats'] = get_numeric_formats()
        item['metadata']['kv_types'] = get_kv_types()

        return item

    @property
    def kv(self):
        return KVNode(instance=self)

    @property
    def kvcomp(self):
        return KVCompNode(instance=self)

    def inherit_kv_from(self, folder):
        instances_set = []

        for key in folder.kv.keys():
            instances_set.append(
                KVStoreNode(key=key, kv_inherited=True, node=self)
            )

        # if there is metadata
        if len(instances_set) > 0:
            diff = Diff(
                operation=Diff.ADD,
                instances_set=instances_set
            )

            self.propagate_changes(
                diffs_set=[diff],
                apply_to_self=True
            )

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.title


class AbstractFolder(models.Model):
    base_ptr = models.ForeignKey(
        Folder,
        related_name=RELATED_NAME_FMT,
        related_query_name=RELATED_QUERY_NAME_FMT,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def get_title(self):
        return self.base_ptr.title
