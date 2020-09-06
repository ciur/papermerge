import time
from django.test import TestCase

from papermerge.core.utils import (
    Timer,
    filter_node_id,
    remove_backup_filename_id
)

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

