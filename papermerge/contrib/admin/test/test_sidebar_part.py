from django.test import TestCase

from papermerge.core.models import Document
from papermerge.contrib import admin

from papermerge.test.utils import create_root_user

from papermerge.test.parts.app_0.models import Document as DocumentPart
from papermerge.test.parts.app_0.models import Color


class AdminSidebarDocumentPart(admin.SidebarPart):
    app_label = 'app_0'
    verbose_name = "App Zero"
    model = DocumentPart

    fields = (
        'extra_special_id',
        'color'
    )


class TestSidebarPart(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_basic(self):
        """
        Asserts that SidebarPart is created
        """
        green = Color.objects.create(name="green")

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

        sidebar_part = AdminSidebarDocumentPart(doc)
        self.assertTrue(sidebar_part)
