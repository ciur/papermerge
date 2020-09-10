from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from papermerge.contrib.admin.models import LogEntry
from papermerge.core.models import Tag

User = get_user_model()


class TestLogViews(TestCase):

    def setUp(self):
        self.user = _create_user(
            username="john",
            password="test"
        )
        self.client = Client()
        self.client.login(
            username='john',
            password='test'
        )

    def test_log_view(self):
        log = LogEntry.objects.create(
            user=self.user, message="test"
        )
        ret = self.client.post(
            reverse('admin:log', args=(log.id,)),
        )
        self.assertEqual(ret.status_code, 200)

        # try to see a non existing log entry
        # must return 404 status code
        ret = self.client.post(
            reverse('admin:log', args=(log.id + 1,)),
        )
        self.assertEqual(ret.status_code, 404)


class TestTagViews(TestCase):

    def setUp(self):
        self.user = _create_user(
            username="john",
            password="test"
        )
        self.client = Client()
        self.client.login(
            username='john',
            password='test'
        )

    def test_tag_view(self):
        log = Tag.objects.create(
            user=self.user, name="test"
        )
        ret = self.client.post(
            reverse('admin:tag', args=(log.id,)),
        )
        self.assertEqual(ret.status_code, 200)

        # try to see a non existing log entry
        # must return 404 status code
        ret = self.client.post(
            reverse('admin:tag', args=(log.id + 1,)),
        )
        self.assertEqual(ret.status_code, 404)


def _create_user(username, password):
    user = User.objects.create_user(
        username=username,
        is_active=True,
    )
    user.set_password(password)
    user.save()

    return user
