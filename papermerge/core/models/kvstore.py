from django.db import models
from papermerge.core.custom_signals import propagate_kv

ADD = 'add'
DEL = 'del'
UPDATE = 'update'


class KV:
    """
    utility class that will operates (adds, deletes, updates, sends propagate)
    on KVStoreNode of Node (Folder or Document)
    or on KVStorePage of the Page
    """

    def __init__(self, instance):
        self.instance = instance

    @property
    def namespace(self):
        """
        returns namepace for added keys
        """
        pass

    def add(self, key):
        """
        adds a namespaced key,
        sends event signal for descendents to update themselves
        """
        self.instance.kvstore.create(
            namespace=self.namespace,
            key=key
        )
        propagate_kv.send(
            sender=self.instance.__class__,
            instance=self.instance,
            key=key,
            namespace=self.namespace,
            operation=ADD
        )

    def delete(self, key):
        """
        adds a namespaced key,
        sends event signal for descendents to update themselves
        """
        self.instance.kvstore.remove(
            key=key
        )
        propagate_kv.send(
            sender=self.instance.__class__,
            instance=self.instance,
            key=key,
            namespace=self.namespace,
            operation=DEL
        )


class KVNode(KV):
    pass


class KVPage(KV):
    pass


class KVStore(models.Model):
    # e.g. shop, price, date
    key = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    # e.g. groceries - full breadcrumb to the current node
    namespace = models.CharField(
        max_length=1024,
        null=True,
        blank=True
    )
    # (namespace, key) = primary key
    # e.g.
    # 1.   groceries_shop
    #      groceries_price
    # 2. key = shop
    #    namespace = clients_retail
    #    namespaced_key = clients_retail_shop
    namespaced_key = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    value = models.TextField(
        null=True,
        blank=True
    )


class KVStoreNode(KVStore):
    node = models.ForeignKey(
        'BaseTreeNode',
        on_delete=models.CASCADE,
        related_name='kvstore'
    )

    def __str__(self):
        k = self.key
        v = self.v
        n = self.node.id
        s = self.namespace
        return f"KVStoreNode(namespace={s}, key={k}, value={v}, node={n})"

    def __repre__(self):
        return str(self)


class KVStorePage(KVStore):
    """
    Normalized KVStore per Page
    """
    page_id = models.ForeignKey(
        'Page',
        on_delete=models.CASCADE
    )
