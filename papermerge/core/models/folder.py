from django.utils.translation import ugettext_lazy as _
from papermerge.core import mixins
from papermerge.core.custom_signals import propagate_kv
from papermerge.core.models.kvstore import ADD, DEL
from papermerge.core.models.node import BaseTreeNode
from papermerge.search import index


class Folder(mixins.ExtractIds, BaseTreeNode):

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

    @property
    def kv_namespace(self):
        """
        returns namepace for added keys
        """
        pass

    def kv_add(self, key):
        """
        adds a namespaced key,
        sends event signal for descendents to update themselves
        """
        self.kvstore.create(
            namespace=self.kv_namespace,
            key=key
        )
        propagate_kv.send(
            sender=self.__class__,
            instance=self,
            key=key,
            namespace=self.kv_namespace,
            operation=ADD
        )

    def kv_del(self, key):
        """
        adds a namespaced key,
        sends event signal for descendents to update themselves
        """
        self.kvstore.remove(
            key=key
        )
        propagate_kv.send(
            sender=self.__class__,
            instance=self,
            key=key,
            namespace=self.kv_namespace,
            operation=DEL
        )

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.title
