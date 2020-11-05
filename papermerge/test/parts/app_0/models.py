from django.db import models

from papermerge.core.models import AbstractDocument


class Document(AbstractDocument):
    """
    This document part adds an extra attribute
    """

    extra_special_id = models.CharField(
        max_length=50,
        unique=True,
        null=True
    )

    def __repr__(self):
        _i = self.id
        _e = self.extra_special_id
        _b = self.base_ptr

        return f"DocumentPart(id={_i}, extra_special_id={_e}, base_ptr={_b})"
