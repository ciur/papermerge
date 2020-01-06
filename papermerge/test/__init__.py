from django.contrib.auth.models import (
    User, Permission
)


def create_root_user():
    user = User.objects.create_user(
        'root',
        'root@mail.com',
        'rootme99',
        is_active=True,
    )

    vml_access = Permission.objects.get(codename='vml_access')
    vml_root = Permission.objects.get(codename='vml_root')
    user.user_permissions.add(vml_access)
    user.user_permissions.add(vml_root)
    user.save()

    return user


def create_margaret_user():
    user = User.objects.create_user(
        'margaret',
        'margaret@mail.com',
        'rootme99',
        is_active=True,
    )

    vml_access = Permission.objects.get(codename='vml_access')
    vml_document = Permission.objects.get(codename='vml_documents')
    vml_change = Permission.objects.get(codename='vml_change')
    user.user_permissions.add(vml_access)
    user.user_permissions.add(vml_document)
    user.user_permissions.add(vml_change)
    user.save()

    return user


def create_uploader_user():
    user = User.objects.create_user(
        'uploader',
        'uploader@mail.com',
        'rootme99',
        is_active=True,
    )

    vml_access = Permission.objects.get(codename='vml_access')
    vml_document = Permission.objects.get(codename='vml_documents')
    vml_change = Permission.objects.get(codename='vml_change')
    user.user_permissions.add(vml_access)
    user.user_permissions.add(vml_change)
    user.user_permissions.add(vml_document)
    user.save()

    return user
