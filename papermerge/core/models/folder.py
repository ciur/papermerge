from django.utils.translation import ugettext_lazy as _
from papermerge.core import mixins
from papermerge.core.models.node import BaseTreeNode
from papermerge.search import index


class Folder(mixins.ExtractIds, BaseTreeNode):

    search_fields = [
        index.SearchField('title'),
        index.SearchField('text', partial_match=True, boost=2),
        index.SearchField('notes')
    ]

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.title
