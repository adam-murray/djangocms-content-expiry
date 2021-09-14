from django.contrib.auth import get_user_model

from djangocms_content_expiry.models import ContentExpiry

from dateutil.relativedelta import relativedelta


def get_authors():
    """
    Helper to return all authors created by content expiry
    """
    User = get_user_model()
    return User.objects.filter(contentexpiry__created_by__isnull=False).distinct()


def version_has_expiry(version):
    """
    Determine if a version has expiry record added
    """
    return getattr(version, "contentexpiry", None)


def create_version_expiry(version):
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


def copy_content_expiry(old_record, new_version):
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


def _get_future_expire_date(modified_date):
    """
     Expire date should be published + one year
    """
    return modified_date + relativedelta(years=1)
