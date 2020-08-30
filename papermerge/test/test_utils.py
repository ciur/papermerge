import time
from django.test import TestCase

from papermerge.core.utils import Timer

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

