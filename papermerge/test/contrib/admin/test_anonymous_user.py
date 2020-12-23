from django.test import TestCase
from django.test import Client
from django.urls import reverse


class TestAnonymousUserView(TestCase):

    def setUp(self):
        self.client = Client()
        # superuser exists, but is not authenticated

    def test_basic_login_view(self):
        """
        Login view renders OK in case of aunonymous user
        """
        ret = self.client.get(reverse('account_login'))

        self.assertEqual(
            ret.status_code,
            200
        )
