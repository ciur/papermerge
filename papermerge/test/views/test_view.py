import os
from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

src_file_path = os.path.join(
    BASE_DIR, "data", "berlin.pdf"
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

    def test_basic_upload_invalid_input(self):
        ret = self.client.post(
            reverse('core:upload')
        )
        # missing input file
        self.assertEqual(ret.status_code, 400)

    def test_basic_upload(self):

        with open(src_file_path, "rb") as fp:
            self.client.post(
                reverse('core:upload'),
                {
                    'file': fp,
                    'parent_id': -1,
                    'name': "berlin.pdf",
                    'language': "deu"
                },
            )
