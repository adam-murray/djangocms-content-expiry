from django.contrib import admin

from cms.test_utils.testcases import CMSTestCase

import datetime

from djangocms_versioning.constants import PUBLISHED

from djangocms_content_expiry.test_utils.polls.factories import PollContentExpiryFactory, UserFactory
from unittest import skip


class ContentExpiryMonkeyPatchTesCase(CMSTestCase):

    @skip("Don't want to test")
    def test_extended_admin_monkey_patch_list_display_expires(self):
        """
        Monkey patch should add expiry column and values to admin menu list display
        """

        from_date = datetime.datetime.now()

        delta_1 = datetime.timedelta(days=1)
        expire_at_1 = from_date + delta_1
        version = PollContentExpiryFactory(expires=expire_at_1, version__state=PUBLISHED)
        request = self.get_request("/")

        version_admin = admin.site._registry[type(version)]
        list_display = version_admin.get_list_display(request)

        # List display field should have been added by monkeypatch
        self.assertIn('expires', list_display)


# class ContentExpiryMonkeyPatchModelTestCase(CMSTestCase):
#
#     def test_monkey_patch_version_copy(self):
#         """
#         Expiry date should be copied to new object when a new version is created
#         """
#
#         from_date = datetime.datetime.now()
#
#         # Record that is expired by 1 day
#         delta_1 = datetime.timedelta(days=1)
#         expire_at_1 = from_date + delta_1
#         version = PollContentExpiryFactory(expires=expire_at_1, version__state=PUBLISHED)
#
#         user = UserFactory()
#
#         new_version = version.copy(user)
#
#         self.assertNotEqual(version.pk, new_version.pk)
#         self.assertEqual(expire_at_1, new_version.expires)
