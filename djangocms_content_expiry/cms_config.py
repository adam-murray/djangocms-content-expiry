from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppConfig, CMSAppExtension
from cms.models import Page


class ContentExpiryCMSExtension(CMSAppExtension):
    def __init__(self):
        self.content_expiry_apps_models = {}

    def configure_app(self, cms_config):
        if hasattr(cms_config, "content_expiry_models"):
            content_expiry_apps_models = getattr(cms_config, "content_expiry_models")
            if isinstance(content_expiry_apps_models, dict):
                self.content_expiry_apps_models.update(content_expiry_apps_models)
            else:
                raise ImproperlyConfigured(
                    "Content Expiry configuration must be a dictionary object"
                )
        else:
            raise ImproperlyConfigured(
                "cms_config.py must have content_expiry_models attribute"
            )


class ContentExpiryAppConfig(CMSAppConfig):
    djangocms_content_expiry_enabled = getattr(
        settings, "DJANGOCMS_CONTENT_EXPIRY_ENABLED", True
    )
    content_expiry_models = {
        Page: ["title"]
    }
