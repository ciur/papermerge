from django.contrib.auth.models import AbstractUser
from django.db import models

from papermerge.core.models import Document


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
