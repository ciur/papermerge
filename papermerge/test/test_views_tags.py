import json
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from papermerge.core.models import (
    Tag,
    Folder
)


from .utils import (
    create_root_user,
)


class TestNodesView(TestCase):
    def setUp(self):

        self.testcase_user = create_root_user()
        self.client = Client()
        self.client.login(testcase_user=self.testcase_user)

    def test_alltags_view(self):
        """
        GET /alltags/

        returns all tags of current user
        """
        Tag.objects.create(
            user=self.testcase_user,
            name="tag1"
        )
        Tag.objects.create(
            user=self.testcase_user,
            name="tag2"
        )

        alltags_url = reverse('core:alltags')

        ret = self.client.get(
            alltags_url,
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(
            ret.status_code,
            200
        )
        tags = json.loads(ret.content)

        self.assertEqual(
            set([
                tag['name'] for tag in tags['tags']
            ]),
            set(["tag2", "tag1"])
        )

    def test_validate_tags_against_xss(self):

        p = Folder.objects.create(
            title="P",
            user=self.testcase_user
        )

        ret = self.client.post(
            reverse('core:tags', args=(p.id, )),
            {
                'tags': [
                    {"name": "xss<script>alert('hi!')</script>"}
                ]
            },
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEquals(
            ret.status_code,
            400
        )

    def test_associate_tags_to_folder(self):

        p = Folder.objects.create(
            title="P",
            user=self.testcase_user
        )

        ret = self.client.post(
            reverse('core:tags', args=(p.id, )),
            {
                'tags': [
                    {"name": "red"},
                    {"name": "green"}
                ]
            },
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

        self.assertEquals(
            ret.status_code,
            200
        )

        found_folders = Folder.objects.filter(
            tags__name__in=["red", "green"]
        ).distinct()

        self.assertEqual(
            found_folders.count(),
            1
        )

