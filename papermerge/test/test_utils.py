import time
from django.test import TestCase

from papermerge.core.utils import (
    Timer,
    filter_node_id,
    remove_backup_filename_id,
)

from papermerge.core.models.utils import group_per_model


class TestTimer(TestCase):

    def test_basic_timer_usage(self):
        """
        This UT just checks that calling Timer() with a context
        manager does not throw any exception/error
        """
        with Timer() as timer:
            time.sleep(0.15)

        msg = f"It took {timer} seconds to complete"

        self.assertTrue(msg)

    def test_filter_node_id(self):
        # invalid values of node id will be
        # filtered out (return None)
        self.assertFalse(
            filter_node_id("sdf")
        )

        self.assertFalse(
            filter_node_id("sdf12")
        )

        self.assertFalse(
            filter_node_id(-1)
        )

        self.assertFalse(
            filter_node_id("-1")
        )

        # valid values for node id will pass
        # and will be returned as integers
        self.assertEqual(
            filter_node_id("12"),
            12
        )

        self.assertEqual(
            filter_node_id(100),
            100
        )

    def test_remove_backup_filename_id(self):
        self.assertEqual(
            remove_backup_filename_id("boox__100"),
            "boox"
        )

        self.assertEqual(
            remove_backup_filename_id("boox_123"),
            "boox"
        )

        self.assertEqual(
            remove_backup_filename_id("60_000_000_years_ago.pdf__123"),
            "60_000_000_years_ago.pdf"
        )

        self.assertEqual(
            remove_backup_filename_id("60____years__ago.pdf__123"),
            "60____years__ago.pdf"
        )

        self.assertEqual(
            remove_backup_filename_id(123),
            123
        )

        self.assertEqual(
            remove_backup_filename_id(None),
            None
        )


# Fake classes used by TestPartsUtils.group_per_model
#
class FakeField:
    def __init__(self, name):
        self.name = name


class FakeMeta1:

    def get_fields(self, include_parents):
        return [
            FakeField("field_1"), FakeField("field_2")
        ]


class FakeMeta2:

    def get_fields(self, include_parents):
        return [
            FakeField("field_3"), FakeField("field_4")
        ]


class FakeModel1:

    _meta = FakeMeta1()

    field_1 = FakeField("field_1")
    field_2 = FakeField("field_2")


class FakeModel2:

    _meta = FakeMeta2()

    field_1 = FakeField("field_3")
    field_2 = FakeField("field_4")


class TestPartsUtils(TestCase):

    def test_group_per_model(self):
        """
        Asserts correct functionality of
            papermerge.core.models.utils.group_per_model
        """
        kwargs = {'x': 1, 'y': 2, 'field_1': "right!"}
        grouped_kw = group_per_model(
            [FakeModel1], **kwargs
        )
        self.assertDictEqual(
            grouped_kw,
            {
                FakeModel1: {
                    'field_1': "right!"
                }
            }
        )

    def test_group_per_model_2(self):
        """
        Asserts correct functionality of
            papermerge.core.models.utils.group_per_model
        """
        kwargs = {
            'x': 1,
            'y': 2,
            'field_1': "right!",
            'field_3': "part_of_model2",
            'field_4': "part_of_model2"
        }
        grouped_kw = group_per_model(
            [FakeModel1, FakeModel2], **kwargs
        )
        self.assertDictEqual(
            grouped_kw,
            {
                FakeModel1: {
                    'field_1': "right!"
                },
                FakeModel2: {
                    'field_3': "part_of_model2",
                    'field_4': "part_of_model2"
                }

            }
        )
