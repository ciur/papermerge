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
