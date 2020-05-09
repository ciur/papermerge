import os
from pathlib import Path
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# points to papermerge.testing folder
BASE_DIR = Path(__file__).parent

src_file_path = os.path.join(
    BASE_DIR, "data", "andromeda.pdf"
)


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

        with open(src_file_path, "rb") as f:
            fin = f.read()
            self.client.post(
                reverse('core:upload'),
                {'file': fin},
            )
