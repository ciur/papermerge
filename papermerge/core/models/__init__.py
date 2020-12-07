from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from papermerge.core.models.automate import Automate
from papermerge.core.models.access import Access
from papermerge.core.models.diff import Diff
from papermerge.core.models.document import Document, AbstractDocument
from papermerge.core.models.folder import Folder
from papermerge.core.models.kvstore import KV, KVPage, KVStoreNode, KVStorePage
from papermerge.core.models.node import BaseTreeNode, AbstractNode
from papermerge.core.models.page import Page
from papermerge.core.models.tags import (
    ColoredTag,
    Tag
)
from papermerge.core.models.role import Role
from papermerge.core.models.sidebar_part import SidebarPart


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = 'get_%s_permissions' % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission
    checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _get_perms_dict(user, perms, obj_list):
    #
    #  Bulk permissions return. Optimization measure
    #  for case when folder contains many files.
    #
    for backend in auth.get_backends():
        if not hasattr(backend, 'get_perms_dict'):
            continue

        return backend.get_perms_dict(user, perms, obj_list)


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission
    checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class User(AbstractUser):
    # increases with every imported document
    # decreases with every deleted document
    # when reaches settings.USER_PROFILE_USER_STORAGE_SIZE
    # no more documents can be imported
    current_storage_size = models.BigIntegerField(default=0)
    mail_secret = models.CharField(
        _('email secret'),
        max_length=150,
        blank=True
    )
    mail_by_user = models.BooleanField(
        _('mail import user'),
        default=False,
        help_text=_(
            "Designates whether "
            "the mail import should consider the email address"
        ),
    )
    mail_by_secret = models.BooleanField(
        _('mail import secret'),
        default=False,
        help_text=_(
            "Designates whether the"
            " mail import should consider the secret"
        ),
    )
    # Role is optional.
    # All users EXCEPT superuser
    # have associated a role
    role = models.ForeignKey(
        'Role',
        verbose_name='role',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_(
            "Determines what operations this user is"
            " authorized to perform."
        )
    )

    def update_current_storage(self):
        user_docs = Document.objects.filter(user=self)
        self.current_storage_size = sum(int(doc.size) for doc in user_docs)
        self.save()

    def get_user_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, 'user')

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        return _user_get_permissions(self, obj, 'group')

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        return _user_has_perm(self, perm, obj)

    def get_perms_dict(self, obj, perms):
        return _get_perms_dict(self, obj, perms)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


__all__ = [
    'User',
    'Role',
    'Folder',
    'Document',
    'AbstractDocument',
    'Page',
    'AbstractNode',
    'BaseTreeNode',
    'Access',
    'Automate',
    'Diff',
    'KV',
    'KVPage',
    'KVStoreNode',
    'KVStorePage',
    'ColoredTag',
    'Tag',
    'SidebarPart',
]
