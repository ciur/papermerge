from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http.response import HttpResponseRedirect

from papermerge.core.models import Automate, Folder

User = get_user_model()


class TestAutomateViewsAuthReq(TestCase):
    def setUp(self):
        self.user = _create_user(
            username="john",
            password="test"
        )
        self.dst_folder = Folder.objects.create(
            title="destination Folder",
            user=self.user
        )

    def test_automate_view(self):
        """
        If user is not authenticated reponse must
        be HttpReponseRedirect (302)
        """
        automate = Automate.objects.create(
            user=self.user,
            name="test",
            dst_folder=self.dst_folder,
            match="XYZ",
            matching_algorithm=Automate.MATCH_ANY,
        )
        ret = self.client.get(
            reverse('admin:automate_change', args=(automate.id,)),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )

    def test_automates_view(self):
        """
        Not accessible to users which are not authenticated
        """
        ret = self.client.post(
            reverse('admin:automates'),
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
            reverse('admin:automates'),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )

class TestAutomateViews(TestCase):

    def setUp(self):
        self.user = _create_user(
            username="john",
            password="test"
        )
        self.dst_folder = Folder.objects.create(
            title="destination Folder",
            user=self.user
        )
        self.client = Client()
        self.client.login(
            username='john',
            password='test'
        )

    def test_automate_change_view(self):
        auto = Automate.objects.create(
            user=self.user,
            name="test",
            dst_folder=self.dst_folder,
            match="XYZ",
            matching_algorithm=Automate.MATCH_ANY,
        )
        ret = self.client.get(
            reverse(
                'admin:automate_change',
                args=(auto.id,)
            ),
        )
        self.assertEqual(ret.status_code, 200)

        ret = self.client.get(
            reverse('admin:automate_change', args=(auto.id + 1,)),
        )
        self.assertEqual(ret.status_code, 404)

    def test_automates_view(self):
        ret = self.client.get(
            reverse('admin:automates')
        )
        self.assertEquals(
            ret.status_code, 200
        )

    def test_delete_automates(self):
        a1 = Automate.objects.create(
            user=self.user,
            name="test1",
            dst_folder=self.dst_folder,
            match="XYZ",
            matching_algorithm=Automate.MATCH_ANY,
        )
        a2 = Automate.objects.create(
            user=self.user,
            name="test2",
            dst_folder=self.dst_folder,
            match="XYZ",
            matching_algorithm=Automate.MATCH_ANY,
        )
        Automate.objects.create(
            user=self.user,
            name="test3",
            dst_folder=self.dst_folder,
            match="XYZ",
            matching_algorithm=Automate.MATCH_ANY,
        )
        ret = self.client.post(
            reverse('admin:automates'),
            {
                'action': 'delete_selected',
                '_selected_action': [a1.id, a2.id],
            }
        )
        self.assertEquals(
            ret.status_code, 200
        )
        # two log entries were deleted
        # only one should remain
        self.assertEqual(
            Automate.objects.filter(
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
