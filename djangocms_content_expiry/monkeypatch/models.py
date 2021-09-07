from djangocms_versioning import constants, models

from djangocms_content_expiry.helpers import create_version_expiry


def new_save(old_save):
    """
    Override the Versioning save method to add the expiration date
    """
    def inner(version, **kwargs):
        old_save(version, **kwargs)
        if version.state == constants.PUBLISHED:
            create_version_expiry(version)
        return version
    return inner


models.Version.save = new_save(models.Version.save)
