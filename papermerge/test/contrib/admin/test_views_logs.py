from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http.response import HttpResponseRedirect

from papermerge.contrib.admin.models import LogEntry

User = get_user_model()


class TestLogViewsAuthReq(TestCase):
    def setUp(self):
        self.user = _create_user(
            username="john",
            password="test"
        )

    def test_log_view(self):
        """
        If user is not authenticated reponse must
        be HttpReponseRedirect (302)
        """
        log = LogEntry.objects.create(
            user=self.user, message="test"
        )
        ret = self.client.post(
            reverse('admin:log-update', args=(log.id,)),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )

    def test_logs_view(self):
        """
        Not accessible to users which are not authenticated
        """
        ret = self.client.post(
            reverse('admin:logs'),
            {
                'action': 'delete_selected',
                '_selected_action': [1, 2],
            }
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )
        # same story for get method
        ret = self.client.get(
            reverse('admin:logs'),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )


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
        ret = self.client.get(
            reverse('admin:log-update', args=(log.id,)),
        )
        self.assertEqual(ret.status_code, 200)

        # try to see a non existing log entry
        # must return 404 status code
        ret = self.client.get(
            reverse('admin:log-update', args=(log.id + 1,)),
        )
        self.assertEqual(ret.status_code, 404)

    def test_logs_view(self):
        ret = self.client.get(
            reverse('admin:logs')
        )
        self.assertEquals(
            ret.status_code, 200
        )

    def test_delete_logs(self):
        log1 = LogEntry.objects.create(
            user=self.user, message="test"
        )
        log2 = LogEntry.objects.create(
            user=self.user, message="test"
        )
        LogEntry.objects.create(
            user=self.user, message="test"
        )
        ret = self.client.post(
            reverse('admin:logs'),
            {
                'action': 'delete_selected',
                '_selected_action': [log1.id, log2.id],
            }
        )
        self.assertEquals(
            ret.status_code, 302
        )
        # two log entries were deleted
        # only one should remain
        self.assertEqual(
            LogEntry.objects.filter(
                user=self.user
            ).count(),
            1
        )


def _create_user(username, password):
    user = User.objects.create_user(
        username=username,
        is_active=True,
    )
    user.set_password(password)
    user.save()

    return user
