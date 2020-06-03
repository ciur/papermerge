from django.db import models

ADD = 'add'
REMOVE = 'remove'
UPDATE = 'update'

"""
# KVStore / Key Value Store
####

 Implementation of metadata associated with Folders, Documents
 and Pages. Metadata can be defined at 3 levels:

    * Page
    * Document
    * Folder

If metadata is defined at Folder level - it will be inherited by all
descending nodes (subfolders and documents) and pages of respective
folders. Think of metadata definition as flowing down as a river.

Metadata is a set of key values. For example, metadata defined
on folder Groceries could be:

    * key1 = date
    * key2 = shop
    * key3 = price

This way, each and every document in Groceries folder (and respective pages)
will have associated those 3 keys. Other parts of application code will
populate the values for those keys.
As result, two page document (say D1) in folder Groceries will have:

 D1 content:
   page1 = key=date   value=03 June 2020
           key=shop   value=lidl
           key=price  value=34.02

   page2 = key=date   value=01 June 2020
           key=shop   value=aldi
           key=price  value=19.00

 Which means D1 is one batch scan of two receipts. Other parts of application
 code might split page1 and page2 from D1 into two recepts documents with one
 page each.

 Groceries receitps are good example of simple KV instances.
 There are other type of KV instances - KVComp, or Key Value Composite.
 Consider a list of bank transactions. A content of document which contains
 bank transctions DX can be described as:

 DX content:

  page1 = key=(date, description, amount)  value=(01 June 2020, aldi, 19.00)
          key=(date, description, amount)  value=(03 June 2020, lidl, 34.02)

Basically DX document's metadata is one composite key. Thus, it would make
sense to create a folder titled say, Bank, create one composite key with 3
parts (keys):

  * compkey1 = (date, description, amount)

With compkey1 create for folder Bank, all folder's documents (and resp. pages)
will have associated multiple instances of compkey1.

There can be ONLY ONE composite key per Entity (E=Page, Node=Folder/Document)

KVComp describe tables. Only one table (compkey) per document is supported.
"""


class KVCompKeyLengthMismatch(Exception):
    pass


class KVCompValidation(Exception):
    pass


class KVComp:
    """
    Utility class that operates - adds, deletes, updates,
    values KVComp entries
    """

    def __init__(self, instance):
        self.instance = instance

    @property
    def namespace(self):
        pass

    def _validate(self, key, value):
        """
        Following validations are performed on the kvcomp:
            1. Both key and values must be instanced of either list of tuple
            2. len(key) > 0
            3. All rows (keys/values) must have same number of components.
            4. Column (key parts) names must match.
        """
        if not isinstance(key, (tuple, list)):
            raise KVCompValidation(
                "KVComp key must be a list or a tuple"
            )

        if not isinstance(value, (tuple, list)):
            raise KVCompValidation(
                "KVComp value must be a list or a tuple"
            )

        if len(key) == 0:
            raise KVCompValidation(
                "KVComp key must have more then 0 columns"
            )

        if self.instance.kvstorecomp.count() > 0:
            # there are other rows
            # compare agains first one
            row = self.instance.kvstorecomp.first()
            if row.kvstore.count() != len(key):
                raise KVCompKeyLengthMismatch(
                    "Existing column count does not match with new key length"
                )

            for kvstore in self.instance.kvstorecomp.all():
                if kvstore.key not in key:
                    k = kvstore.key
                    raise KVCompValidation(
                        f"Existing column name does not match for {k}"
                    )

    def add(self, key, value=()):

        self._validate(key, value)

        # creates one row in the table
        new_row = self.instance.kvstorecomp.create()

        # add columns to the table
        for index, k in enumerate(key):
            if len(value) == len(key):
                new_row.kvstore.create(
                    namespace=self.namespace,
                    key=k,
                    value=value[index]
                )
            else:  # means value is empty, but key not
                new_row.kvstore.create(
                    namespace=self.namespace,
                    key=k,
                )

        new_row.save()



class KVCompNode(KVComp):
    pass


class KVCompPage(KVComp):
    pass


class KV:
    """
    Utility class that operates - adds, deletes, updates,
    values KV entries on KVStoreNode of Node (Folder or Document)
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


class KVStoreCompItem(KVStore):
    comp_item = models.ForeignKey(
        'KVStoreCompNode',
        on_delete=models.CASCADE,
        related_name='kvstore',
        null=True,
        blank=True
    )


class KVStoreCompNode(models.Model):
    node = models.ForeignKey(
        'BaseTreeNode',
        on_delete=models.CASCADE,
        related_name='kvstorecomp',
        null=True,
        blank=True
    )
