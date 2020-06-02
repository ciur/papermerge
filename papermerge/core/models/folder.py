from django.utils.translation import ugettext_lazy as _
from papermerge.core import mixins
from papermerge.core.models import kvstore, node
from papermerge.core.signals import propagate_kv
from papermerge.search import index


class Folder(mixins.ExtractIds, node.BaseTreeNode):

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
            namepace=self.kv_namespace,
            key=key
        )
        propagate_kv.send(
            sender=self,
            key=key,
            namespace=self.kv_namespace,
            operation=kvstore.ADD
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
            sender=self,
            key=key,
            namespace=self.kv_namespace,
            operation=kvstore.DEL
        )

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.title
