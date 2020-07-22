import io

from django.contrib.auth import get_user_model
from django.test import TestCase
from papermerge.core.models import Automate, Folder

User = get_user_model()


def _create_am(match, alg, user, is_sensitive):
    dst_folder = Folder.objects.create(
        title="destination Folder",
        user=user
    )
    return Automate.objects.create(
        match=match,
        matching_algorithm=alg,
        is_case_sensitive=is_sensitive,  # i.e. ignore case
        user=user,
        dst_folder=dst_folder
    )


def _create_am_any(match, user):
    return _create_am(
        match=match,
        alg=Automate.MATCH_ANY,
        user=user,
        is_sensitive=False
    )


def _create_am_literal(match, user):
    return _create_am(
        match=match,
        alg=Automate.MATCH_LITERAL,
        user=user,
        is_sensitive=False
    )

class TestAutomateModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin')

    def test_automate_match_literal(self):
        am = _create_am_literal(
            "one",
            self.user
        )
        hocr = """
            He says, one - this text should match!
        """
        self.assertTrue(
            am.is_a_match(hocr)
        )

    def test_automate_match_all(self):
        pass

    def test_automate_match_any(self):
        pass

    def test_automate_match_regexp(self):
        pass





