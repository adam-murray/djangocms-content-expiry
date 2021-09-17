from datetime import datetime

from dateutil.relativedelta import relativedelta

from djangocms_versioning import constants

from djangocms_content_expiry.models import ContentExpiry


def create_content_expiry(**kwargs):
    if kwargs['operation'] == constants.OPERATION_DRAFT:
        version = kwargs["obj"]
        if not hasattr(version, "contentexpiry"):
            ContentExpiry.objects.create(
                version=version,
                created=version.created,
                created_by=version.created_by,
                expires=_get_future_expire_date(datetime.now()),
            )


def _get_future_expire_date(modified_date):
    """
     Expire date should be published + one year
    """
    return modified_date + relativedelta(years=1)
