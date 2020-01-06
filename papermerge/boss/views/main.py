from django.contrib.admin.views.main import ChangeList
from django.urls import reverse
from django.contrib.admin.utils import (
    quote
)
from papermerge.core import models
from django.contrib.admin.views.main import IGNORED_PARAMS

VIEW_TYPE = 'vt'


class ChangeListBoss(ChangeList):

    def url_for_result(self, result):
        pk = getattr(result, self.pk_attname)

        node = models.BaseTreeNode.objects.get(id=quote(pk))

        if node.is_leaf_node() and isinstance(node, models.Document):
            return super().url_for_result(result)

        return reverse('admin:%s_%s_changelist_obj' % (
            self.opts.app_label,
            self.opts.model_name),
            args=(quote(pk),),
            current_app=self.model_admin.admin_site.name
        )

    def get_filters_params(self, params=None):
        """
        Return all params except IGNORED_PARAMS.

        This function removes IGNORED_PARAMS from
        request parameters. I introduced also param vt (viewtype)
        (vt = list | grid), this is why I override django's method.
        """
        if not params:
            params = self.params
        lookup_params = params.copy()  # a dictionary of the query string
        # Remove all the parameters that are globally and systematically
        # ignored.
        IGNORED_PARAMS_EX = IGNORED_PARAMS + (VIEW_TYPE,)
        for ignored in IGNORED_PARAMS_EX:
            if ignored in lookup_params:
                del lookup_params[ignored]

        return lookup_params
