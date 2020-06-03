from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from papermerge.core.models.access import Access
from papermerge.core.models.access_diff import AccessDiff
from polymorphic_tree.models import (PolymorphicMPTTModel,
                                     PolymorphicTreeForeignKey)


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

    def _get_access_diff_updated(self, new_access_list=[]):
        """
        gathers AccessDiff with updated operation
        """
        updates = AccessDiff(op=AccessDiff.UPDATE)

        for current in self.access_set.all():
            for new_access in new_access_list:
                if new_access == current and current.perm_diff(new_access):
                    updates.add(new_access)

        return updates

    def _get_access_diff_deleted(self, new_access_list=[]):
        """
        gathers AccessDiff with deleted operation
        """
        dels = AccessDiff(op=AccessDiff.DELETE)

        # if current access is not in the new list
        # it means current access was deleted.
        for current in self.access_set.all():
            if current not in new_access_list:
                dels.add(current)

        return dels

    def _get_access_diff_added(self, new_access_list=[]):
        """
        gathers AccessDiff with added operation
        """
        adds = AccessDiff(op=AccessDiff.ADDED)

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

    def _apply_access_diff_add(self, access_diff):
        if access_diff.is_add():
            for access in access_diff:
                Access.create(
                    node=self,
                    access_inherited=True,
                    access=access
                )

    def _apply_access_diff_delete(self, access_diff):
        if access_diff.is_delete():
            ids_to_delete = []
            for existing_access in self.access_set.all():
                for new_access in access_diff:
                    if existing_access == new_access:
                        ids_to_delete.append(
                            existing_access.id
                        )
            Access.objects.filter(id__in=ids_to_delete).delete()

    def _apply_access_diff_update(self, access_diff):
        if access_diff.is_update():
            for existing_access in self.access_set.all():
                for new_access in access_diff:
                    existing_access.update_from(new_access)

    def apply_access_diff(self, access_diff):
        self._apply_access_diff_add(access_diff)
        self._apply_access_diff_update(access_diff)
        self._apply_access_diff_delete(access_diff)

    def replace_access_diff(self, access_diff):
        # delete exiting
        self.access_set.all().delete()

        # replace with new ones
        for access in access_diff:
            Access.create(
                node=self,
                access_inherited=True,
                access=access
            )

    def apply_access_diffs(self, access_diffs):
        for x in access_diffs:
            if x.is_update() or x.is_add() or x.is_delete():
                # add (new), update (existing) or delete(existing)
                self.apply_access_diff(x)
            elif x.is_replace():
                self.replace_access_diff(x)

    def update_kv(self, key, operation):
        pass

    def propagate_kv(
        self,
        key,
        operation,
        apply_to_self=False
    ):
        if apply_to_self:
            self.update_kv(key, operation)

        for node in self.get_descendants():
            node.update_kv(key, operation)

    def propagate_access_changes(
        self,
        access_diffs,
        apply_to_self
    ):
        """
        Adds new_access permission to self AND all children.
        """

        if apply_to_self:
            self.apply_access_diffs(access_diffs)

        children = self.get_children()
        if children.count() > 0:
            for node in children:
                node.apply_access_diffs(access_diffs)
                node.propagate_access_changes(
                    access_diffs,
                    apply_to_self=False
                )

    class Meta(PolymorphicMPTTModel.Meta):
        # please do not confuse this "Documents" verbose name
        # with real Document object, which is derived from BaseNodeTree.
        # The reason for this naming confusing is that from the point
        # of view of users, the BaseNodeTree are just a list of documents.
        verbose_name = _("Documents")
        verbose_name_plural = _("Documents")
        _icon_name = 'basetreenode'
