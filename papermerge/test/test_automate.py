from django.contrib.auth import get_user_model
from django.test import TestCase
from papermerge.core.models import (
    Automate,
    Folder,
    Document
)
from papermerge.core.models.page import get_pages
from papermerge.core.models.folder import get_inbox_children

User = get_user_model()


TEXT = """
The majority of mortals, Paulinus, complain bitterly of the spitefulness of
Nature, because we are born for a brief span of life, because even this space
that has been granted to us rushes by so speedily and so swiftly that all save
a very few find life at an end just when they are getting ready to live.

Seneca - On the shortness of life
"""


class TestAutomateModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin')

    def test_automate_match_literal(self):
        am_1 = _create_am_literal(
            "1",
            "Paulinus",
            self.user
        )
        am_2 = _create_am_literal(
            "2",
            "Cesar",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )

    def test_automate_match_all(self):
        # should match because all words occur in
        # text
        am_1 = _create_am_all(
            "1",
            "granted life rushes",
            self.user
        )
        # should not mach, because word quality
        # is not in TEXT
        am_2 = _create_am_all(
            "2",
            "granted life quality rushes",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )

    def test_automate_match_any(self):
        # should match by word 'granted'

        am_1 = _create_am_any(
            "1",
            "what if granted usecase test",
            self.user
        )
        # should not mach, of none of the words
        # is found in TEXT
        am_2 = _create_am_any(
            "2",
            "what if usecase test",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )

    def test_automate_match_any2(self):

        am_1 = _create_am_any(
            "schnell",
            "schnell",
            self.user,
            is_case_sensitive=False
        )
        result = am_1.is_a_match(
            """
            SCHNELL

            IHRE FAMILIENBÄCKEREI
            """
        )
        self.assertTrue(result)

    def test_automate_match_any3(self):

        am_1 = _create_am_any(
            "schnell",
            "schnell",
            self.user,
            is_case_sensitive=True
        )
        result = am_1.is_a_match(
            """
            SCHNELL

            IHRE FAMILIENBÄCKEREI
            """
        )
        # will not match because text contains
        # uppercase version, while text to match is expected
        # to be lowercase as is_case_sensitive=True
        self.assertFalse(result)

    def test_automate_match_regex(self):
        # should match by word life.
        am_1 = _create_am_any(
            "1",
            r"l..e",
            self.user
        )
        # should not mach, there no double digits
        # in the TEXT
        am_2 = _create_am_any(
            "2",
            r"\d\d",
            self.user
        )
        self.assertTrue(
            am_1.is_a_match(TEXT)
        )
        self.assertFalse(
            am_2.is_a_match(TEXT)
        )

    def test_automate_apply(self):
        """
        test automate.apply method
        """

        # automates are applicable only for documents
        # in inbox folder
        folder, _ = Folder.objects.get_or_create(
            title=Folder.INBOX_NAME,
            user=self.user
        )
        document = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder.id,
            page_count=5,
        )
        document2 = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder.id,
            page_count=5,
        )
        # automate with tags
        automate = _create_am_any("test", "test", self.user)
        automate.tags.set(
            "test", "one", tag_kwargs={'user': self.user}
        )
        # make sure no exception is rised
        automate.apply(
            document=document,
            page_num=1,
            text="test",
        )
        # without tags
        automate2 = _create_am_any("test2", "test", self.user)

        # make sure no exception is rised
        automate2.apply(
            document=document2,
            page_num=1,
            text="test",
        )

    def test_automate_run_from_queryset(self):
        folder, _ = Folder.objects.get_or_create(
            title=Folder.INBOX_NAME,
            user=self.user
        )
        Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder.id,
            page_count=2,
        )
        doc = Document.objects.create_document(
            title="document_c",
            file_name="document_c.pdf",
            size='1212',
            lang='DEU',
            user=self.user,
            parent_id=folder.id,
            page_count=1,
        )
        page = doc.pages.first()
        page.text = TEXT
        page.save()
        # automate with tags
        _create_am_any(
            name="test",
            match="Paulinus",
            user=self.user
        )
        matched_automates = Automate.objects.all().run(
            get_pages(
                get_inbox_children(self.user),
                include_pages_with_empty_text=False
            )
        )

        self.assertEquals(
            matched_automates.count(),
            1
        )


def _create_am(name, match, alg, user, **kwargs):
    dst_folder = Folder.objects.create(
        title="destination Folder",
        user=user
    )
    return Automate.objects.create(
        name=name,
        match=match,
        matching_algorithm=alg,
        user=user,
        dst_folder=dst_folder,
        **kwargs
    )


def _create_am_any(name, match, user, **kwargs):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_ANY,
        user=user,
        **kwargs
    )


def _create_am_all(name, match, user):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_ALL,
        user=user,
        is_case_sensitive=False
    )


def _create_am_literal(name, match, user):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_LITERAL,
        user=user,
        is_case_sensitive=False
    )


def _create_am_regex(name, match, user):
    return _create_am(
        name=name,
        match=match,
        alg=Automate.MATCH_REGEX,
        user=user,
        is_case_sensitive=False
    )
