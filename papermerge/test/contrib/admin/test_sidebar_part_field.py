from django.test import TestCase

from papermerge.core.models import Document
from papermerge.contrib import admin

from papermerge.test.utils import create_root_user

from papermerge.test.parts.app_0.models import Color
from papermerge.test.parts.app_0.models import Document as DocumentPart


class TestSidebarFieldPart(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_get_internal_type(self):
        green = Color.objects.create(name="green")
        # other colors are available as well
        red = Color.objects.create(name="red")
        yellow = Color.objects.create(name="yellow")

        doc = Document.objects.create_document(
            file_name="test.pdf",
            title="Test #1",
            page_count=3,
            size="3",
            lang="DEU",
            user=self.user,
            parts={
                "extra_special_id": "DOC_XYZ_1"
            }
        )
        doc.parts.color = green

        sidebar_field_1 = admin.SidebarPartField(
            document=doc,  # core document instance
            field_name="extra_special_id",
            model=DocumentPart,
        )

        sidebar_field_2 = admin.SidebarPartField(
            document=doc,  # core document instance
            field_name="color",
            model=DocumentPart,
            options={
                'color': {
                    'choice_fields': [
                        'id', 'name'
                    ]
                }
            }
        )

        self.assertEqual(
            sidebar_field_1.get_internal_type(),
            "CharField",  # sticks with django model field names conversions
        )

        self.assertEqual(
            sidebar_field_2.get_internal_type(),
            "ForeignKey",  # sticks with django model field names conversions
        )

        self.assertEqual(
            sidebar_field_1.get_value(),
            "DOC_XYZ_1"
        )

        self.assertDictEqual(
            sidebar_field_1.to_json(),
            {
                "class": "CharField",
                "value": "DOC_XYZ_1",
                "field_name": "extra_special_id"
            }
        )

        self.assertEqual(
            sidebar_field_2.get_value(),
            green
        )

        self.assertDictEqual(
            sidebar_field_2.to_json(),
            {
                "class": "ForeignKey",
                "value": (green.id, green.name),
                "choices": [
                    (green.id, green.name),
                    (red.id, red.name),
                    (yellow.id, yellow.name),
                ],
                "field_name": "color"
            }
        )
