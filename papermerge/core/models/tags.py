from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.models import TagBase, GenericTaggedItemBase


class Tag(TagBase):
    bg_color = models.CharField(
        max_length=6,     # RGB color in hex notation
        default='00FF00'  # green
    )

    fg_color = models.CharField(
        max_length=6,     # RGB color in hex notation
        default='FFFFFF'  # white
    )

    # each user has his/her set of tags
    user = models.ForeignKey('User', models.CASCADE)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def to_dict(self):
        return {
            'bg_color': self.bg_color,
            'fg_color': self.fg_color,
            'name': self.name,
        }


class ColoredTag(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
