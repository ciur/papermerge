from django.db import models

ADD = 'add'
REMOVE = 'remove'
UPDATE = 'update'


class KVComp:
    def __init__(self, instance):
        self.instance = instance

    def add(self, key):
        pass


class KVCompNode(KVComp):
    pass


class KVCompPage(KVComp):
    pass


class KV:
    """
    Utility class that operates - adds, deletes, updates,
    sends propagate signals - on KVStoreNode of Node (Folder or Document)
    and on KVStorePage of the Page
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
        self.propagate(key=key, operation=ADD)

    def remove(self, key):
        """
        adds a namespaced key,
        sends event signal for descendents to update themselves
        """
        self.instance.kvstore.filter(key=key).delete()
        self.propagate(key=key, operation=ADD)

    def propagate(self, key, operation):
        self.instance.propagate_kv(
            key=key,
            operation=operation
        )


class KVNode(KV):
    """
    KV specific to Node (Folder or Document)
    """
    pass


class KVPage(KV):
    """
    KV specific to Page
    """
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

    # inherited kv is read only
    kv_inherited = models.BooleanField(
        default=False
    )


class KVStoreNode(KVStore):
    node = models.ForeignKey(
        'BaseTreeNode',
        on_delete=models.CASCADE,
        related_name='kvstore',
        null=True
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


class KVStoreCompItem(models.Model):
    comp_item = models.ForeignKey(
        'KVStore',
        on_delete=models.CASCADE,
        related_name='kvstore',
        null=True
    )


class KVStoreCompNode(models.Model):
    node = models.ForeignKey(
        'BaseTreeNode',
        on_delete=models.CASCADE,
        related_name='kvstorecomp',
        null=True
    )
