from dateutil.relativedelta import relativedelta

from djangocms_versioning import models

from djangocms_content_expiry.models import ContentExpiry


def new_save(old_save):
    """
    Override the Versioning save method to add the expiration date
    """
    def inner(version, **kwargs):
        old_save(version, **kwargs)

        # Check if version has content expiry added
        new_version = _version_has_expiry(version)
        if new_version is None:
            # If version does not have an expiry record, it needs to be created
            _create_version_expiry(version)
        else:
            # Content expiry object exists so copying the original expiry object
            old_expiry_record = ContentExpiry.objects.filter(version_id=version.source_id)
            _copy_content_expiry(old_expiry_record, version)
        return version
    return inner


models.Version.save = new_save(models.Version.save)


def _copy_content_expiry(old_record, new_version):
    """
    Create a content expiry record with existing expiry date
    """
    version = ContentExpiry.objects.get_or_create(
        version=new_version,
        created=new_version.created,
        created_by=new_version.created_by,
        expires=old_record[0].expires
    )
    return version


def _create_version_expiry(version):
    """
    Helper to create a new entry in versioning with the expiration date
    """
    ContentExpiry.objects.get_or_create(
        version=version,
        created=version.created,
        created_by=version.created_by,
        expires=_get_future_expire_date(version.modified)
    )
    return version


def _get_future_expire_date(modified_date):
    """
     Expire date should be published + one year
    """
    return modified_date + relativedelta(years=1)


def _version_has_expiry(version):
    """
    Determine if a version has expiry record added
    """
    return getattr(version, "contentexpiry", None)
