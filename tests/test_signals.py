from cms.test_utils.testcases import CMSTestCase
from cms.test_utils.util.context_managers import signal_tester

import datetime
from unittest import skip

from djangocms_versioning.constants import DRAFT

from djangocms_content_expiry.test_utils.polls.factories import PollContentExpiryFactory

from djangocms_versioning import signals


class ContentExpirySignalTestCase(CMSTestCase):
    # TODO: Finish the test
    @skip("Test not complete")
    def test_submitted_for_review_signal(self):
        """
        Test that creating a new version emits a signal
        """
        delta = datetime.timedelta(days=31)
        expire = datetime.datetime.now() + delta
        PollContentExpiryFactory(expires=expire, version__state=DRAFT)
        with signal_tester(signals.post_version_operation) as env:
            self.assertEqual(env.call_count, 1)
