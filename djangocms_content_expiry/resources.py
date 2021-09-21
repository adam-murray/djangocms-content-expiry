from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from import_export import resources
from import_export.fields import Field

from .models import ContentExpiry


class ContentExpiryResource(resources.ModelResource):
    title = Field(column_name=_("Title"))
    content_type = Field(column_name=_("Content Type"))
    version_state = Field(column_name=_("Version State"))
    expires = Field(attribute='expires', column_name=_("Expire Date"))
    version_author = Field(column_name=_("Version Author"))

    def dehydrate_title(self, obj):
        return obj.version.content

    def dehydrate_content_type(self, obj):
        return ContentType.objects.get_for_model(
            obj.version.content
        )

    def dehydrate_version_state(self, obj):
        return obj.version.get_state_display()

    def dehydrate_version_author(self, obj):
        return obj.version.created_by

    class Meta:
        model = ContentExpiry
        fields = ('title', 'content_type', 'expires', 'version_state', 'version_author',)
