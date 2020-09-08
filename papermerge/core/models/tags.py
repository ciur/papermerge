from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.models import TagBase, GenericTaggedItemBase


class Tag(TagBase):
    bg_color = models.CharField(
        _("Background Color"),
        max_length=7,     # RGB color in hex notation
        default='#c41fff',  # purple,
    )

    fg_color = models.CharField(
        _("Foreground Color"),
        max_length=7,      # RGB color in hex notation
        default='#FFFFFF'  # white
    )

    description = models.TextField(
        _("Description (optional)"),
        max_length=1024,
        blank=True,
        null=True
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
