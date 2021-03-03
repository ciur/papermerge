from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Permission
)

from papermerge.core.models import (
    Document,
    Role
)

User = get_user_model()


def create_root_user():
    user = User.objects.create_user(
        'admin',
        'admin@mail.com',
        is_active=True,
        is_superuser=True,
    )
    user.save()

    return user


def create_margaret_user():
    user = User.objects.create_user(
        'margaret',
        'margaret@mail.com',
        is_active=True,
    )
    user.save()

    return user


def create_user(username: str, perms: list) -> User:
    """
    Creates a user and assigns given set of permissions.

    Perms is alist of permission names (as strings).
    For example:

    ['auth.view_group', 'auth.change_group']
    """
    user = User.objects.create_user(
        username,
        is_active=True
    )

    role = Role.objects.create(
        name=f"{username}_role"
    )

    for perm_name in perms:
        app_label, codename = perm_name.split('.')
        perm = Permission.objects.get(
            content_type__app_label=app_label,
            codename=codename
        )
        role.permissions.add(perm)

    role.save()
    user.role = role
    user.save()

    return user


def create_elizabet_user():
    user = User.objects.create_user(
        'elizabet',
        'elizabet@mail.com',
        is_active=True,
    )
    user.save()

    return user


def create_uploader_user():
    user = User.objects.create_user(
        'uploader',
        'uploader@mail.com',
        is_active=True,
    )
    user.save()

    return user


def create_some_doc(
    user,
    page_count=2,
    parent_id=None,
    title="document_A"
):
    """
    Returns a (newly created) document instance.
    Title, file_name, size, language do not matter.
    """
    doc = Document.objects.create_document(
        title=title,
        file_name="document_A.pdf",
        size='36',
        lang='DEU',
        user=user,
        page_count=page_count,
        parent_id=parent_id
    )

    return doc
