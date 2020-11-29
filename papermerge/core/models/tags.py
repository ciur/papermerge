from django.db import models
from django.utils.translation import ugettext_lazy as _

from papermerge.core import validators

from taggit.models import TagBase, GenericTaggedItemBase
from taggit.managers import TaggableManager


class UserTaggableManager(TaggableManager):
    """
    Taggable manager for models with user attribute.

    Model with user attribute means following: that model (say MO) is per user.
    Because tags are per User as well - they (tags) will need to get
    (inherit) user instance from respective model (MO). For this reason,
    save_from_data method is overriden - it passes user attribut to the newly
    saved tag model.

    Example: automate model is per user:

        class Automate(models.Model):
            ...
            tags = UserTaggableManager(
                through=ColoredTag,
                blank=True  # tags are optional
            )
            ...
            user = models.ForeignKey(
                'User',
                models.CASCADE,
                blank=True,
                null=True
            )
            ...
    )
    """

    def save_form_data(self, instance, value):
        rel = getattr(instance, self.name)

        if hasattr(instance, 'user'):
            rel.set(*value, tag_kwargs={'user': instance.user})
        else:
            rel.set(*value)


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

    # a pinned tag may be displayed for example under "Documents" menu
    # of left side bar. It serves as shortcut for user to quickly filter
    # folders/documents with that particular tag.
    pinned = models.BooleanField(
        default=False,
        help_text=_(
            "Pinned tag will be displayed under Documents menu. "
            "It serves as shortcut to quickly filter "
            "folders/documents associated with this tag"
        )
    )

    # each user has his/her set of tags
    user = models.ForeignKey('User', models.CASCADE)
    name = models.CharField(
        verbose_name=_("name"),
        unique=False,
        max_length=100,
        validators=[validators.safe_character_validator]
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ['name']
        unique_together = ['name', 'user']

    def to_dict(self):
        return {
            'bg_color': self.bg_color,
            'fg_color': self.fg_color,
            'name': self.name,
            'description': self.description,
            'pinned': self.pinned
        }


class ColoredTag(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
