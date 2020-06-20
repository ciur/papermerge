from django.test import TestCase
from papermerge.core.templatetags.search_tags import highlight, search_excerpt

#  Discourses of Epictetus
TEXT = """
    Of things some are in our power, and others are not. In our power
    are opinion, movement towards a thing, desire, aversion, turning
    from a thing; and in a word, whatever are our acts.
    Not in our power are the body, property, reputation, offices
    (magisterial power), and in a word, whatever are not our own acts.
    And the things in our power are by nature free, not subject to
    restraint or hindrance; but the things not in our power are weak,
    slavish, subject to restraint, in the power of others.
"""


class TestSearchExcerpt(TestCase):
    """ This is not testing of search feature!

        This TestCase tests core functions of search_except_tag templatetag:

            * search_excerpt
            * highlight
    """

    def test_search_excerpt_basic(self):

        result = search_excerpt(
            text=TEXT,
            phrases="weak",
            context_words_count=2
        )

        self.assertEqual(
            result['excerpt'],
            "... power are weak, slavish, subject ..."
        )

    def test_search_excerpt_two_phrases(self):
        result = search_excerpt(
            text=TEXT,
            phrases=["weak", "free"],
            context_words_count=2
        )

        self.assertEqual(
            result['excerpt'],
            "... by nature free, not subject ..."
            " power are weak, slavish, subject ..."
        )

    def test_search_excerpt_phrase_occurs_twice(self):
        result = search_excerpt(
            text=TEXT,
            phrases=["others"],
            context_words_count=2
        )

        self.assertEqual(
            result['excerpt'],
            "... power, and others are not. ..."
        )

    def test_highlight(self):
        result = highlight(
            text="this is a weak match",
            phrases=["weak"],
            class_name="highlighted"
        )

        self.assertEqual(
            result['highlighted'],
            'this is a <span class="highlighted">weak</span> match'
        )
