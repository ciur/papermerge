from django.contrib.auth.models import (
    User,
    Permission,
)
from django.contrib.contenttypes.models import ContentType


def create_boss_perms():
    """
    """

    permissions = (
        ('vml_documents', "Documents", ),
        ('vml_tasks', "Tasks", ),
        ('vml_groups', "Groups", ),
        ('vml_users', "Users", ),
        ('vml_root', "Root", ),
        ('vml_access', "Access", ),
        ('vml_change', "Change", ),
    )

    # a dummy
    content_type, _ = ContentType.objects.get_or_create(
        app_label="core",
        model="subscription",
    )

    vml_access, _ = Permission.objects.get_or_create(
        codename="vml_access",
        name="Access",
        content_type=content_type
    )

    vml_root, _ = Permission.objects.get_or_create(
        codename="vml_root",
        name="Root",
        content_type=content_type

    )

    for perm in permissions:
        Permission.objects.get_or_create(
            codename=perm[0],
            name=perm[1],
            content_type=content_type
        )

    return vml_access, vml_root


def create_boss_root_user(
    username,
    password,
    email
):
    """
    Boss root user is the user is created when anonymous user
    register to the application. This function is used in tests.
    """

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    vml_access, vml_root = create_boss_perms()
    user.user_permissions.add(vml_access)
    user.user_permissions.add(vml_root)

    user.save()

    return user
