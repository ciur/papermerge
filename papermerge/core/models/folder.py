from django.utils.translation import ugettext_lazy as _

from papermerge.core import mixins
from papermerge.core.models.node import BaseTreeNode


class Folder(mixins.ExtractIds, BaseTreeNode):

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.title
