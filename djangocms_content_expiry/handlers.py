from datetime import datetime

from dateutil.relativedelta import relativedelta

from djangocms_versioning import constants
from djangocms_versioning.models import Version

from djangocms_content_expiry.models import ContentExpiry


def create_content_expiry(**kwargs):
    new_version = kwargs["obj"]
    expiry_record = None

    # Get latest version
    version = Version.objects.filter(version=new_version).last()
    if version:
        # Get expiry record for the version
        expiry_record = ContentExpiry.objects.filter(version=version)

    if expiry_record is not None:
        # Copy existing expiry record to new version
        ContentExpiry.objects.create(
            version=new_version,
            created=new_version.created,
            created_by=new_version.created_by,
            expires=expiry_record[0].expires
        )
    else:
        # Add content expiry as it does not exist
        if kwargs['operation'] == constants.OPERATION_DRAFT:
            ContentExpiry.objects.create(
                version=new_version,
                created=new_version.created,
                created_by=new_version.created_by,
                expires=_get_future_expire_date(datetime.now())
            )


def _get_future_expire_date(modified_date):
    """
     Expire date should be published + one year
    """
    return modified_date + relativedelta(years=1)
