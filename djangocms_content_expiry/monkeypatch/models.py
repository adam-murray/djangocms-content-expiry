from djangocms_versioning import models

from djangocms_content_expiry.helpers import copy_content_expiry, create_version_expiry, version_has_expiry
from djangocms_content_expiry.models import ContentExpiry

from djangocms_versioning.constants import DRAFT, PUBLISHED
from djangocms_versioning.models import Version
from djangocms_versioning import versionables


def new_save(old_save):
    """
    Override the Versioning save method to add the expiration date
    """
    def inner(version, **kwargs):
        old_save(version, **kwargs)

        # Check if version has content expiry added
        new_version = version_has_expiry(version)

        if new_version is not None:
            # If version does not have an expiry record, it needs to be created
            create_version_expiry(version)
        else:
            # Content expiry object exists so copying the original expiry object
            old_expiry_record = ContentExpiry.objects.filter(version_id=version.source_id)
            copy_content_expiry(old_expiry_record, version)
        return version
    return inner


models.Version.save = new_save(models.Version.save)
