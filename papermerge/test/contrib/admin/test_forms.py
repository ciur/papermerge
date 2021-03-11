from django.test import TestCase

from papermerge.core.models import Automate, Folder
from papermerge.contrib.admin.forms import AutomateForm
from papermerge.test.utils import create_root_user


class TestForms(TestCase):

    def setUp(self):
        self.user = create_root_user()

    def test_basic_automate_form(self):
        # automate form can be called with or without
        # user as argument
        form = AutomateForm(user=self.user)
        self.assertTrue(form)

        form = AutomateForm()
        self.assertTrue(form)

        folder = Folder.objects.create(
            title="FolderX",
            user=self.user
        )
        automate = Automate(
            user=self.user,
            name="XYZ",
            match="X",
            matching_algorithm=Automate.MATCH_ANY,
            dst_folder=folder
        )
        automate.save()

        form = AutomateForm(instance=automate)
        self.assertTrue(form)
