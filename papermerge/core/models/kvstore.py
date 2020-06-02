from django.db import models


class KVStore(models.Model):
    # e.g. shop, price, date
    key = models.CharField(
        max_length=200,
    )
    # e.g. groceries - full breadcrumb to the current node
    namespace = models.CharField(
        max_length=1024
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
        primary_key=True,
        db_index=True,
        unique=True
    )

    value = models.TextField()

    # human readable key
    human_key = models.CharField(
        max_length=200
    )


class KVStoreNode(KVStore):
    node_id = models.ForeignKey(
        'BaseTreeNode',
        on_delete=models.CASCADE
    )


class KVStorePage(KVStore):
    """
    Normalized KVStore per Page
    """
    page_id = models.ForeignKey(
        'Page',
        on_delete=models.CASCADE
    )
