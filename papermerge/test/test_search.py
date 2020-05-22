from django.test import TestCase
from django.contrib.auth import get_user_model
from papermerge.core.models import (
    Document,
)

from papermerge.search.backends import get_search_backend

User = get_user_model()

class TestPage(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test')

    def test_search_backend(self):
        backend = get_search_backend()
        backend.search("Great doc!", Document)

