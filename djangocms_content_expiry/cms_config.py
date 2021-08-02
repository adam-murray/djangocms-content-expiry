from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from cms.app_base import CMSAppConfig, CMSAppExtension
from cms.models import Page
from cms.utils.i18n import get_language_tuple

from .models import ContentExpiryContent


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
    djangocms_content_expiry_enabled = True
    djangocms_versioning_enabled = getattr(
        settings, "DJANGOCMS_CONTENT_EXPIRY_VERSIONING_ENABLED", True
    )
    djangocms_moderation_enabled = getattr(
        settings, "DJANGOCMS_CONTENT_EXPIRY_MODERATION_ENABLED", True
    )
    content_expiry_models = {
        Page: ["title"]
    }
    if djangocms_versioning_enabled:
        from djangocms_versioning.datastructures import VersionableItem, default_copy

        versioning = [
            VersionableItem(
                content_model=ContentExpiryContent,
                grouper_field_name="content_type",
                version_list_filter_lookups={"language": get_language_tuple},
                copy_function=default_copy
            )
        ]
