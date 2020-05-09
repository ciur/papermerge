from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class TestBasicUpload(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='john',
            is_active=True,
        )
        self.user.set_password('test')
        self.user.save()
        self.client = Client()
        self.client.login(
            username='john',
            password='test'
        )

    def test_basic_upload(self):
        ret = self.client.post(
            reverse('core:upload')
        )
        # missing input file
        self.assertEqual(ret.status_code, 400)
