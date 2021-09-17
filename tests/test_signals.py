from cms.api import create_page
from cms.test_utils.testcases import CMSTestCase

from djangocms_versioning.models import Version

from djangocms_content_expiry.models import ContentExpiry


class ContentExpirySignalTestCase(CMSTestCase):
    def test_content_expiry_creation_signal(self):
        """
        Test that creating a new version emits the signal to create a content expiry record
        """
        language = "en"
        user = self.get_superuser()
        page = create_page(
            title="home",
            template="page.html",
            language=language,
            created_by=user
        )

        version = Version.objects.filter_by_grouper(page)
        expiry_record = ContentExpiry.objects.filter(version=version[0])
        self.assertEqual(len(expiry_record), 1)
        self.assertTrue(hasattr(expiry_record[0], "expires"))
