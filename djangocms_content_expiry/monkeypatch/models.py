from djangocms_versioning import models

from djangocms_content_expiry.helpers import create_version_expiry, version_has_expiry

from djangocms_versioning.constants import DRAFT
from djangocms_versioning.models import Version


def new_save(old_save):
    """
    Override the Versioning save method to add the expiration date
    """
    def inner(version, **kwargs):
        old_save(version, **kwargs)

        # Check if version has content expiry added
        new_version = version_has_expiry(version)
        if new_version is not None and version.state != DRAFT:
            # If version does not have an expiry record, it needs to be created
            version = create_version_expiry(version)
        else:
            # Content expiry object exists so copying the original expiry object
            version = Version.object.filter(version=version.pk).copy(version.created_by)
        return version
    return inner


models.Version.save = new_save(models.Version.save)
