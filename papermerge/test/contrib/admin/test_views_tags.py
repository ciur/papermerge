from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http.response import (
    HttpResponseRedirect,
)

from papermerge.core.models import Tag

User = get_user_model()


class TestTagsViewsAuthReq(TestCase):
    def setUp(self):
        self.user = _create_user(
            username="john",
            password="test"
        )

    def test_tag_view(self):
        """
        If user is not authenticated reponse must
        be HttpReponseRedirect (302)
        """
        tag = Tag.objects.create(
            user=self.user, name="test"
        )
        ret = self.client.get(
            reverse('admin:tag-update', args=(tag.pk,)),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )

    def test_tags_view(self):
        """
        Not accessible to users which are not authenticated
        """
        ret = self.client.post(
            reverse('admin:tags'),
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
            reverse('admin:tags'),
        )
        self.assertEqual(
            ret.status_code,
            HttpResponseRedirect.status_code
        )


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

    def test_tag_change_view(self):
        tag = Tag.objects.create(
            user=self.user, name="test"
        )
        ret = self.client.get(
            reverse('admin:tag-update', args=(tag.pk,)),
        )
        self.assertEqual(ret.status_code, 200)

        # try to see a non existing log entry
        # must return 404 status code
        ret = self.client.get(
            reverse('admin:tag-update', args=(tag.pk + 1,)),
        )
        self.assertEqual(ret.status_code, 404)

    def test_tags_view(self):
        ret = self.client.get(
            reverse('admin:tags')
        )
        self.assertEqual(
            ret.status_code, 200
        )

    def test_delete_tags(self):
        tag1 = Tag.objects.create(
            user=self.user, name="test1"
        )
        tag2 = Tag.objects.create(
            user=self.user, name="test2"
        )
        Tag.objects.create(
            user=self.user, name="test3"
        )
        ret = self.client.post(
            reverse('admin:tags'),
            {
                'action': 'delete_selected',
                '_selected_action': [tag1.id, tag2.id],
            }
        )
        self.assertEqual(
            ret.status_code, 302
        )
        # two tags entries were deleted
        # only one should remain
        self.assertEqual(
            Tag.objects.filter(
                user=self.user
            ).count(),
            1
        )

    def test_tags_view_user_adds_duplicate_tag(self):
        """
        User will try to
        add a duplicate. In case of duplicate - a user friendly
        error will be displayed
        """
        Tag.objects.create(
            user=self.user, name="tag-10"
        )
        # do it again
        ret = self.client.post(
            reverse('admin:tag-add'),
            {
                'name': 'tag-10',
                'pinned': False,
                'fg_color': '#000000',
                'bg_color': '#FF0000'
            }
        )
        # no dramatic exception here, like DB duplicate key
        # violations
        self.assertEqual(
            ret.status_code,
            200
        )
        # no new tags were added
        self.assertEqual(
            Tag.objects.count(),
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
