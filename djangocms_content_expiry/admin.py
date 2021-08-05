from django.contrib import admin
from django.conf.urls import url
from django.utils.translation import ugettext, ugettext_lazy as _

from djangocms_content_expiry.models import ContentExpiry
from djangocms_versioning.admin import ExtendedVersionAdminMixin

from .views import PreviewView


@admin.register(ContentExpiry)
class ContentExpiryAdmin(ExtendedVersionAdminMixin, admin.ModelAdmin):
    list_display = ['content_type', 'from_expiry_date', 'to_expiry_date']
    fieldsets = (
            (None, {
                'fields': ('content_type', 'from_expiry_date', 'to_expiry_date')
            }),
        )

    verbose_name = _("Content")
    verbose_name_plural = _("Contents")

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        return [
            url(
                r"^(?P<id>\d+)/preview/$",
                self.admin_site.admin_view(PreviewView.as_view()),
                name="{}_{}_preview".format(*info),
            )
        ] + super().get_urls()
