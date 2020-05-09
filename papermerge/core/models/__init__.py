from django.contrib.auth.models import AbstractUser
from django.db import models

from papermerge.core.models.document import Document
from papermerge.core.models.folder import Folder
from papermerge.core.models.page import Page
from papermerge.core.models.node import BaseTreeNode


class User(AbstractUser):
    # increases with every imported document
    # decreases with every deleted document
    # when reaches settings.USER_PROFILE_USER_STORAGE_SIZE
    # no more documents can be imported
    current_storage_size = models.BigIntegerField(default=0)

    def update_current_storage(self):
        user_docs = Document.objects.filter(user=self)
        self.current_storage_size = sum(int(doc.size) for doc in user_docs)
        self.save()


__all__ = [
    'User',
    'Folder',
    'Document',
    'Page',
    'BaseTreeNode'
]
