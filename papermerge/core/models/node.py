from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from papermerge.core.models.access import Access
from papermerge.core.models.diff import Diff
from papermerge.core.models.kvstore import KVStoreCompNode, KVStoreNode
from polymorphic_tree.models import (PolymorphicMPTTModel,
                                     PolymorphicTreeForeignKey)

# things you can propagate from parent node to
# child node
PROPAGATE_ACCESS = 'access'
PROPAGATE_KV = 'kv'
PROPAGATE_KVCOMP = 'kvcomp'


class BaseTreeNode(PolymorphicMPTTModel):
    parent = PolymorphicTreeForeignKey(
        'self',
        models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('parent')
    )
    title = models.CharField(
        _("Title"),
        max_length=200
    )

    lang = models.CharField(
        _('Language'),
        max_length=8,
        blank=False,
        null=False,
        default='deu'
    )

    user = models.ForeignKey('User', models.CASCADE)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # Obsolete columns. Replaced by ancestors_fts
    ancestors_deu = SearchVectorField(null=True)
    ancestors_eng = SearchVectorField(null=True)
    # Obsolete columns. Replaced by title_fts
    title_deu = SearchVectorField(null=True)
    title_eng = SearchVectorField(null=True)

    # this column is updated by update_fts command
    ancestors_fts = SearchVectorField(null=True)
    title_fts = SearchVectorField(null=True)

    def is_folder(self):
        folder_ct = ContentType.objects.get(
            app_label='core', model='folder'
        )
        return self.polymorphic_ctype_id == folder_ct.id

    def is_document(self):
        document_ct = ContentType.objects.get(
            app_label='core', model='document'
        )
        return document_ct.id == self.polymorphic_ctype_id

    def _get_access_diff_updated(self, new_access_list=[]):
        """
        gathers Diff with updated operation
        """
        updates = Diff(op=Diff.UPDATE)

        for current in self.access_set.all():
            for new_access in new_access_list:
                if new_access == current and current.perm_diff(new_access):
                    updates.add(new_access)

        return updates

    def _get_access_diff_deleted(self, new_access_list=[]):
        """
        gathers Diff with deleted operation
        """
        dels = Diff(op=Diff.DELETE)

        # if current access is not in the new list
        # it means current access was deleted.
        for current in self.access_set.all():
            if current not in new_access_list:
                dels.add(current)

        return dels

    def _get_access_diff_added(self, new_access_list=[]):
        """
        gathers Diff with added operation
        """
        adds = Diff(op=Diff.ADDED)

        # if current access is not in the new list
        # it means current access was deleted.
        all_current = self.access_set.all()

        # if new access is not in current access list of the
        # node - it means it will be added.
        for new_access in new_access_list:
            if new_access not in all_current:
                adds.add(new_access)

        return adds

    def get_access_diffs(self, new_access_list=[]):
        """
        * access_list is a list of Access model instances.

        Returns a list of instances of AccessDiff
        between current node access list and given access list.

        Returned value will be empty list if access_list is same
        as node's current access.
        Returned value will be a list with one entry if one or
        several access were added.
        Returned value will be a list with one entry if one or
        several access were removed.
        Returned value will be a list with two entries if one or
        several access were added and one or several entries were
        removed.
        """
        ret = []
        ret.append(
            self._get_access_diff_updated(new_access_list)
        )
        ret.append(
            self._get_access_diff_added(new_access_list)
        )
        ret.append(
            self._get_access_diff_deleted(new_access_list)
        )

        return ret

    def _apply_diff_add(self, diff):
        model = diff.first()
        if isinstance(model, Access):
            for _model in diff:
                Access.create(
                    node=self,
                    access_inherited=True,
                    access=_model
                )
        elif isinstance(model, KVStoreNode):
            self.kv.apply_additions(
                [
                    {'kv_inherited': True, 'key': _model.key}
                    for _model in diff
                ]
            )
        elif isinstance(model, KVStoreCompNode):
            pass
        else:
            raise ValueError(
                f"Don't know how to replace {model} (found in {diff})"
            )

    def _apply_diff_delete(self, diff):
        ids_to_delete = []
        model = diff.first()

        if isinstance(model, Access):
            for existing_model in self.access_set.all():
                for new_model in diff:
                    if existing_model == new_model:
                        ids_to_delete.append(
                            existing_model.id
                        )
            Access.objects.filter(id__in=ids_to_delete).delete()
        elif isinstance(model, KVStoreNode):
            self.kv.apply_deletions(
                [
                    {'kv_inherited': True, 'key': _model.key}
                    for _model in diff
                ]
            )
        elif isinstance(model, KVStoreCompNode):
            pass
        else:
            raise ValueError(
                f"Don't know how to replace {model} (found in {diff})"
            )

    def _apply_diff_update(self, diff, attr_updates):
        model = diff.first()
        if isinstance(model, Access):
            for existing_model in self.access_set.all():
                for new_model in diff:
                    existing_model.update_from(new_model)
        elif isinstance(model, KVStoreNode):

            if len(attr_updates) > 0:
                updates = attr_updates
            else:
                updates = [{
                    'kv_inherited': True,
                    'key': _model.key,
                    'kv_format': _model.format,
                    'kv_type': _model.type,
                    'id': _model.id
                } for _model in diff]

            self.kv.apply_updates(updates)
        elif isinstance(model, KVStoreCompNode):
            pass
        else:
            raise ValueError(
                f"Don't know how to replace {model} (found in {diff})"
            )

    def apply_diff(self, diff, attr_updates):
        if diff.is_add():
            self._apply_diff_add(diff)
        elif diff.is_update():
            self._apply_diff_update(diff, attr_updates)
        elif diff.is_delete():
            self._apply_diff_delete(diff)
        else:
            raise ValueError("Unexpected diff {diff} type")

    def replace_access(self, diff):
        # delete exiting
        self.access_set.all().delete()

        # replace with new ones
        for access in diff:
            Access.create(
                node=self,
                access_inherited=True,
                access=access
            )

    def replace_kv(self, diff):
        pass

    def replace_kvcomp(self, diff):
        pass

    def replace_diff(self, diff):
        model = diff.first()

        if isinstance(model, Access):
            self.replace_access(diff)
        elif isinstance(model, KVStoreNode):
            # replace associated kv of current node
            # with new one specified by diff elements
            self.replace_kv(diff)
        elif isinstance(model, KVStoreCompNode):
            # replace associated kvcomp of current node
            # with new one specified by diff elements
            self.replace_kvcomp(diff)
        else:
            raise ValueError(
                f"Don't know how to replace {model} (found in {diff})"
            )

    def apply_diffs(self, diffs_list, attr_updates):
        for diff in diffs_list:
            if diff.is_update() or diff.is_add() or diff.is_delete():
                # add (new), update (existing) or delete(existing)
                self.apply_diff(diff, attr_updates)
            elif diff.is_replace():
                self.replace_diff(diff)

    def update_kv(self, key, operation):
        pass

    def propagate_changes(
        self,
        diffs_set,
        apply_to_self,
        attr_updates=[]
    ):
        """
        Recursively propagates list of diffs
        (i.e. apply changes to all children).
        diffs_set is a set of papermerge.core.models.Diff instances
        """

        if apply_to_self:
            self.apply_diffs(
                diffs_set,
                attr_updates=attr_updates
            )

        children = self.get_children()
        if children.count() > 0:
            for node in children:
                node.apply_diffs(
                    diffs_set,
                    attr_updates=attr_updates
                )
                node.propagate_changes(
                    diffs_set,
                    apply_to_self=False,
                    attr_updates=attr_updates
                )

    class Meta(PolymorphicMPTTModel.Meta):
        # please do not confuse this "Documents" verbose name
        # with real Document object, which is derived from BaseNodeTree.
        # The reason for this naming confusing is that from the point
        # of view of users, the BaseNodeTree are just a list of documents.
        verbose_name = _("Documents")
        verbose_name_plural = _("Documents")
        _icon_name = 'basetreenode'
