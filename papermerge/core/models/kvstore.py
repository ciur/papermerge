import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from .diff import Diff
from papermerge.core.utils import (
    date_2int,
    money_2int,
    number_2int
)

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

Metadata is defined as a set of key names of specific type and format.
For example, metadata defined on folder Groceries could be:

    * key1 = date / type=date / format dd.mm.yy
    * key2 = shop / type=text / format=N/A
    * key3 = price / type=money / format dd,cc

This way, each and every document in Groceries folder (and respective pages)
will have associated those 3 keys. Other parts of application code will
populate the values for those keys.
As result, two page document (say D1) in folder Groceries will have:

 D1 content:
   page1 = key=date   value=03.06.2020
           key=shop   value=lidl
           key=price  value=34,02

   page2 = key=date   value=01.06.20
           key=shop   value=aldi
           key=price  value=19,00

 Which means D1 is one batch scan of two receipts. Other parts of application
 code might split page1 and page2 from D1 into two receipts documents with one
 page each.

 Groceries receitps are good example of simple KV instances.
 There are other type of KV instances - KVComp, or Key Value Composite.
 Consider a list of bank transactions. A content of document (DX)
 which contains bank transctions can be described as:

 DX content:

  page1 = key=(date, description, amount)  value=(01 June 2020, aldi, 19.00)
          key=(date, description, amount)  value=(03 June 2020, lidl, 34.02)

Basically DX document's metadata is one composite key. Thus, it would make
sense to create a folder titled say, Bank, create one composite key with 3
parts (keys):

  * compkey1 = (date, description, amount)

With compkey1 created for folder Bank, all folder's documents (and resp. pages)
will have associated multiple instances of compkey1.

There can be ONLY ONE composite key per Entity (E=Page, Node=Folder/Document)

KVComp describe tables. I repeat, as this is important -
only one table (compkey) per document is supported.
"""


logger = logging.getLogger(__name__)

# metadata types
TEXT = 'text'
MONEY = 'money'
NUMERIC = 'numeric'
DATE = 'date'

METADATA_TYPES = (
    (TEXT, _("Freeform Text")),
    (MONEY, _("Monetary")),
    (NUMERIC, _("Numeric")),
    (DATE, _("Date"))
)


def compute_virtual_value(kv_type, kv_format, value):
    """
    See comments for KVStore.virtual_value.
    In case of error, unknown kv_type, unkown kv_format,
    or error during conversion - log error and return 0.
    """
    result = 0
    if kv_type == DATE:
        result = date_2int(kv_format, value)
    elif kv_type == MONEY:
        result = money_2int(kv_format, value)
    elif kv_type == NUMERIC:
        result = number_2int(kv_format, value)
    elif kv_type == TEXT:
        # virtual_value is not used for kv_type=TEXT
        result = 0
    else:
        logger.error("Unknown kv_type value")
        return 0

    return result


def get_kv_types():
    return METADATA_TYPES


def get_currency_formats():
    return [
        (currency, _(currency))
        for currency in settings.PAPERMERGE_METADATA_CURRENCY_FORMATS
    ]


def get_numeric_formats():
    return [
        (numeric, _(numeric))
        for numeric in settings.PAPERMERGE_METADATA_NUMERIC_FORMATS
    ]


def get_date_formats():
    return [
        (_date, _(_date))
        for _date in settings.PAPERMERGE_METADATA_DATE_FORMATS
    ]


class KVCompKeyLengthMismatch(Exception):
    pass


class KVCompValidation(Exception):
    pass


class TypedKey:
    """ Used to compare inherited keys
    from parent to child (or from doc to page).
    Correcly inherited key is not just a key name - it is
    a combination of key, type and format.
    """

    def __init__(self, key, ktype, kformat):
        self.key = key
        self.ktype = ktype
        self.kformat = kformat

    def __eq__(self, other):

        _key = (self.key == other.key)
        _type = (self.ktype == other.ktype)
        _format = (self.kformat == other.kformat)

        return _key and _type and _format

    def __hash__(self):
        return hash((self.key, self.ktype, self.kformat))

    def __str__(self):
        return f"TypedKey({self.key}, {self.ktype}, {self.kformat})"

    def __repr__(self):
        return f"TypedKey({self.key}, {self.ktype}, {self.kformat})"


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

    def all(self):
        result = []
        for row in self.instance.kvstorecomp.all():
            result.append(row.kvstore.all())

        return result

    def update(self, data):
        """
        data is one of:
            *
            *
        """
        pass

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

    ADD = 'add'
    REMOVE = 'remove'
    UPDATE = 'update'

    class MetadataKeyDoesNotExist(Exception):
        """
        Raised when assigning (e.g. page.kv['shop'] = y)
        or retrieving a not existing metadata key - in example above - 'shop'
        """
        pass

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
        instance = self.instance.kvstore.create(
            namespace=self.namespace,
            key=key
        )
        self.propagate(
            instances_set=[instance],
            operation=Diff.ADD
        )

    def __setitem__(self, key, value):

        try:
            instance = self.instance.kvstore.get(key=key)
        except Exception:
            raise KV.MetadataKeyDoesNotExist(
                f"Metadata key '{key}' does not exist."
            )

        if instance:
            instance.value = value
            instance.save()

    def __getitem__(self, key):
        try:
            instance = self.instance.kvstore.get(key=key)
        except Exception:
            raise KV.MetadataKeyDoesNotExist(
                f"Metadata key '{key}' does not exist."
            )

        if instance:
            return instance.value

        return None

    def keys(self):
        return [
            item.key for item in self.all()
        ]

    def typed_keys(self):
        return [
            item.to_typed_key() for item in self.all()
        ]

    def get_diff(self, data):
        result = {}
        result[KV.ADD] = []
        result[KV.REMOVE] = []
        result[KV.UPDATE] = []
        present_keys = self.keys()

        # discard empty string keys
        data = list(
            filter(lambda item: len(item['key']) > 0, data)
        )
        for item in data:
            if item['key'] not in present_keys:
                if item.get('id', False):
                    # key is not present, but it has an id => it is an update
                    result[KV.UPDATE].append(item)
                else:
                    # key is not present and it has no ID => it is new
                    result[KV.ADD].append(item)
            elif item.get('id', False):
                # presence of id attributes means an update.
                result[KV.UPDATE].append(item)

        # other way around (check for removes)
        data_keys = [item['key'] for item in data]
        for item in self.all():
            # if existing item's key is not found in data

            if item.key not in data_keys:
                # neither its id is found
                id_found = next(
                    filter(lambda x: x.get('id', False) == item.id, data),
                    False
                )
                # it means that user opted for key removal.
                if not id_found:
                    result[KV.REMOVE].append({
                        'key': item.key,
                        'id': item.id
                    })

        return result

    def apply_updates(self, updates):
        """
        updates is a list of dictionaries. Each dict is a will contain
        a key named "key" and one named "id" - the attributes of kvstore to be
        updated.
        """
        if len(updates) == 0:
            return

        attr_updates = []
        for item in updates:
            # update exiting
            if 'id' in item:
                kvstore_node = self.instance.kvstore.filter(
                    id=item['id']
                ).first()
                if kvstore_node:
                    # ok found it, just update the key
                    attr_updates.append({
                        # old key is needed in order to find the element
                        'old': kvstore_node.key,
                        'new': item['key'],
                        'kv_format': item['kv_format'],
                        'kv_type': item['kv_type'],
                        'value': item.get('value', None)
                    })
                    kvstore_node.key = item['key']
                    kvstore_node.kv_format = item['kv_format']
                    kvstore_node.kv_type = item['kv_type']
                    if item.get('value', False):
                        kvstore_node.value = item.get('value')
                    kvstore_node.save()
            elif 'old' in item and 'new' in item:
                kvstore_node = self.instance.kvstore.filter(
                    key=item['old']
                ).first()
                if kvstore_node:
                    # ok found it, just update the key
                    attr_updates.append({
                        'old': kvstore_node.key,
                        'new': item['new'],
                        'kv_format': item['kv_format'],
                        'kv_type': item['kv_type'],
                        'value': item.get('value', None)
                    })
                    kvstore_node.key = item['new']
                    kvstore_node.kv_format = item['kv_format']
                    kvstore_node.kv_type = item['kv_type']
                    if item.get('value', False):
                        kvstore_node.value = item.get('value')
                    kvstore_node.save()

        # It does not make sense to continue
        # propagation in case of pages.
        # Pages are leafs so to speak of hierarchy tree.
        # Thus propagation stops here.
        if isinstance(self, KVPage):
            return

        if updates:
            prop_updates = []
            for item in updates:
                if 'key' in item:
                    prop_updates.append(
                        KVStoreNode(
                            key=item['key'],
                            kv_type=item.get('kv_type', None),
                            kv_format=item.get('kv_format', None),
                        )
                    )
            self.propagate(
                instances_set=prop_updates,
                operation=Diff.UPDATE,
                attr_updates=attr_updates
            )

    def apply_additions(self, new_additions):
        """
        new_additions is a list of dictionaries. Each dict is a will contain
        a key named "key" - the key of kvstore to be added.
        """
        for item in new_additions:
            # look up by key
            kvstore_node = self.instance.kvstore.filter(
                key=item['key']
            ).first()
            # this key does not exist for this node
            if not kvstore_node:
                # delete a python id key regardless if it is present
                # or not.
                # The point here is that NEW element is created, so
                # presense of empty id key raises an error.
                item.pop('id', None)
                self.instance.kvstore.create(**item)
                self.instance.save()

        if new_additions:
            new_additions = [
                KVStoreNode(**item)
                for item in new_additions
            ]
            self.propagate(
                instances_set=new_additions,
                operation=Diff.ADD
            )

    def apply_deletions(self, deletions):
        """
        deletions is a list of dictionaries. Each dict is a will contain
        a key named "key" - the key of kvstore to be deleted.
        """
        for item in deletions:
            # look up by key
            kvstore_node = self.instance.kvstore.filter(
                key=item['key']
            ).first()
            self.instance.kvstore.remove(kvstore_node)

        if deletions:
            deletions = [
                KVStoreNode(key=item['key'])
                for item in deletions
            ]
            self.propagate(
                instances_set=deletions,
                operation=Diff.DELETE
            )

    def update(self, data):
        """
        data is one of:
            * list of dictionaries
        a dict can contain KVStore fields like:

            'key' = kvstore.key
            'id' = kvstore.id
        """

        if len(data) == 0:
            return

        kv_diff = self.get_diff(data)

        self.apply_updates(
            kv_diff[KV.UPDATE]
        )
        self.apply_additions(
            kv_diff[KV.ADD]
        )
        self.apply_deletions(
            kv_diff[KV.REMOVE]
        )

    def all(self):
        return self.instance.kvstore.all()

    def count(self):
        return self.instance.kvstore.count()

    def remove(self, key):
        """
        adds a namespaced key,
        sends event signal for descendents to update themselves
        """
        instances = self.instance.kvstore.filter(key=key)
        instances.delete()
        self.propagate(
            instances_set=[instances],
            operation=Diff.DELETE
        )

    def propagate(
        self,
        instances_set,
        operation,
        attr_updates=[]
    ):
        kv_diff = Diff(
            operation=operation,
            instances_set=instances_set
        )
        self.instance.propagate_changes(
            diffs_set=[kv_diff],
            apply_to_self=False,
            attr_updates=attr_updates
        )


class KVNode(KV):
    """
    KV specific to Node (Folder or Document)
    """

    def __eq__(self, kvnode):
        """
        Two KVNodes are equal if all conditions
        are true:
        * kvnode is attached to the same node
        * have name number of keys
        * keys names are same
        """
        if self.kv.instance.id != kvnode.instance.id:
            return False

        if len(self.kv.all()) != len(kvnode.instance.kv.all()):
            return False

        keys_set1 = set(self.kv.keys())
        keys_set2 = set(kvnode.kv.keys())
        if keys_set1 != keys_set2:
            return False

        return True


class KVPage(KV):
    """
    KV specific to Page
    """

    def apply_additions(self, new_additions):
        """
        new_additions is a list of dictionaries. Each dict is a will contain
        a key named "key" - the key of kvstore to be added.
        """
        for item in new_additions:
            # look up by key
            kvstore_node = self.instance.kvstore.filter(
                key=item['key']
            ).first()
            # this key does not exist for this node
            if not kvstore_node:
                self.instance.kvstore.create(**item)


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

    kv_type = models.CharField(
        max_length=16,
        choices=[
            (TEXT, _('Text')),
            (MONEY, _('Currency')),
            (NUMERIC, _('Numeric')),
            (DATE, _('Date'))
        ],
        default='text'
    )

    # Format for kv_type
    #
    # e.g. for currency => dd.cc or may be dd,cc
    #      for date => dd.mm.yy or dd Month YYYY
    #      for numeric => 1,2000 or 1200 or 1.200
    #
    # available formats are loaded from configuration file
    # and will be displayed for user to choose from when
    # creating/adding a metadata.
    #
    # Without specifing format - metadata is basically useless.
    # what does value=05.06.20 key=date mean ?
    # is it 5th of June 2020 or it is 6th of May 2020 ?
    kv_format = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )

    # inherited kv is read only
    kv_inherited = models.BooleanField(
        default=False
    )

    def to_dict(self):
        item = {}
        item['id'] = self.id
        item['key'] = self.key
        item['kv_type'] = self.kv_type
        item['kv_format'] = self.kv_format
        item['kv_inherited'] = self.kv_inherited
        item['value'] = self.value
        item['virtual_value'] = self.virtual_value
        item['kv_types'] = get_kv_types()
        item['currency_formats'] = get_currency_formats()
        item['numeric_formats'] = get_numeric_formats()
        item['date_formats'] = get_date_formats()

        return item

    def to_typed_key(self):

        return TypedKey(
            key=self.key,
            ktype=self.kv_type,
            kformat=self.kv_format
        )

    @property
    def virtual_value(self):
        """
        An integer number e.g. 1, 100, 345 which is used for sorting.
        It is deduced from 3 components: (value, kv_type, kv_format).

        Example:
        given two metadata items:

            m1 = (date, 'dd.mm.yy', '04.05.20')
            m2 = (date, 'dd.mm.yy', '05.06.20')

        How to order them? Well, here is where virtual_value comes into
        the picture. Virtual value is computed, as integer number,
        and based on it, m1 and m2 are ordered.
        """
        result = compute_virtual_value(
            self.kv_type,
            self.kv_format,
            self.value
        )
        return result


class KVStoreNode(KVStore):
    node = models.ForeignKey(
        'BaseTreeNode',
        on_delete=models.CASCADE,
        related_name='kvstore',
        null=True
    )

    def __str__(self):
        k = self.key
        v = self.value
        if self.node:
            n = self.node.id
        else:
            n = None
        s = self.namespace
        f = self.kv_format
        t = self.kv_type

        return f"KVStoreNode(namespace={s}," + \
            f" key={k}, kv_type={t}, kv_format={f}, value={v}, node={n})"

    def __repr__(self):
        return str(self)


class KVStorePage(KVStore):
    """
    Normalized KVStore per Page
    """
    page = models.ForeignKey(
        'Page',
        on_delete=models.CASCADE,
        related_name='kvstore',
        null=True
    )

    def __str__(self):
        k = self.key
        v = self.value
        p = self.page.id
        s = self.namespace
        f = self.kv_format
        t = self.kv_type

        return f"KVStorePage(namespace={s}," + \
            f" key={k}, kv_type={t}, kv_format={f} , value={v}, page={p})"

    def __repr__(self):
        return str(self)


class KVStoreCompItem(KVStore):
    comp_item = models.ForeignKey(
        'KVStoreCompNode',
        on_delete=models.CASCADE,
        related_name='kvstore',
        null=True,
        blank=True
    )

    def __str__(self):
        k = self.key
        v = self.value
        s = self.namespace
        return f"KVStoreCompItem(namespace={s}, key={k}, value={v})"

    def __repre__(self):
        return str(self)


class KVStoreCompNode(models.Model):
    node = models.ForeignKey(
        'BaseTreeNode',
        on_delete=models.CASCADE,
        related_name='kvstorecomp',
        null=True,
        blank=True
    )
