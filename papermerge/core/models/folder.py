from django.utils.translation import ugettext_lazy as _
from papermerge.core import mixins
from papermerge.core.models.diff import Diff
from papermerge.core.models.kvstore import KVCompNode, KVNode, KVStoreNode
from papermerge.core.models.node import BaseTreeNode
from papermerge.search import index


class Folder(mixins.ExtractIds, BaseTreeNode):

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

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
