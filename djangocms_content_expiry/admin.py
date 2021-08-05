from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from djangocms_content_expiry.models import ContentExpiry


@admin.register(ContentExpiry)
class ContentExpiryAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'from_expiry_date', 'to_expiry_date']
    fieldsets = (
            (None, {
                'fields': ('content_type', 'from_expiry_date', 'to_expiry_date')
            }),
        )

    verbose_name = _("Content")
    verbose_name_plural = _("Contents")
