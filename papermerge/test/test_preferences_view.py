from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http.response import (
    HttpResponseRedirect
)


from .utils import (
    create_root_user,
)


class TestPreferencesView(TestCase):

    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_preferences_get(self):
        ret = self.client.get(
            reverse('core:preferences'),
        )
        self.assertEquals(
            ret.status_code,
            200
        )

    def test_preferences_post(self):
        ret = self.client.post(
            reverse('core:preferences'),
            {
                'views__documents_view': 'list',
                'ocr__OCR_Language': 'eng'
            }
        )
        self.assertEquals(
            ret.status_code,
            HttpResponseRedirect.status_code
        )
