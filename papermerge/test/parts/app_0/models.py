from django.db import models

from papermerge.core.models import AbstractDocument


class Color(models.Model):

    name = models.CharField(
        max_length=50
    )

    def __repr__(self):
        return f"Color(name={self.name})"


class Document(AbstractDocument):
    """
    This document part adds an extra attribute
    """

    extra_special_id = models.CharField(
        max_length=50,
        unique=True,
        null=True
    )

    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __repr__(self):

        attrs = {
            'id': self.id,
            'extra_special_id': self.extra_special_id,
            'base_ptr': self.base_ptr,
            'color': self.color
        }

        attributes = ""
        for k, v in attrs.items():
            attributes = f"{attributes},{k}={v}"

        return f"DocumentPart({attributes})"
