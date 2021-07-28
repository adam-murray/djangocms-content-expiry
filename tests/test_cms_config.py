from unittest.mock import Mock

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from djangocms_content_expiry import cms_config


class AppRegistrationTestCase(TestCase):
    def test_missing_cms_config(self):
        extensions = cms_config.ContentExpiryCMSExtension()
        config = Mock(
            djangocms_content_expiry_enabled=True, app_config=Mock(label="test")
        )

        with self.assertRaises(ImproperlyConfigured):
            extensions.configure_app(config)

