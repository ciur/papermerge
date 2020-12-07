from django.db import models
from django.contrib.auth.models import Permission


class Role(models.Model):
    """
    Named set of permissions.

    Role allows you quickly create a user of specific type i.e with
    preset permissions.
    Example: A manager role assigned to user will empower him/her to
    create, update, delete other users.
    Another example: a guest role - might have a very minimal set of
    permissions suitable only for demo mode.
    """

    name = models.CharField(max_length=64)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissions',
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
