from django.contrib.auth import get_user_model

from papermerge.core.models import Document

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


def create_some_doc(user, page_count=2):
    """
    Returns a (newly created) document instance.
    Title, file_name, size, language do not matter.
    """
    doc = Document.create_document(
        title="document_A",
        file_name="document_A.pdf",
        size='36',
        lang='DEU',
        user=user,
        page_count=page_count,
    )

    return doc
