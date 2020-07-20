from django.contrib.auth import get_user_model

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
