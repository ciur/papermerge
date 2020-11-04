from django.db import models

from papermerge.core.models import AbstractNode


class Policy(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    # policy dictates if specific document
    # may be deleted.
    allow_delete = models.BooleanField(
        default=False
    )

    def __str__(self):

        n = self.name
        d = self.allow_delete

        return f"Policy({n}, allow_delete={d})"


class Node(AbstractNode):
    """
    All nodes may have one retention
    policy associated
    """
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name='states',
        blank=True,
        null=True
    )
