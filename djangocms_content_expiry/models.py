from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime


# Temporary placeholder
TYPE_CHOICES = (("Page", "Page"), ("Alias", "Alias"),)


class ContentExpiry(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return "{} ({})".format(self.name, self.pk)


class ContentExpiryContent(models.Model):
    page_type = models.ForeignKey(ContentExpiry, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )
    from_expiry_date = models.DateField(_("From Expiry Date"), default=datetime.date.today)
    to_expiry_date = models.DateField(_("To Expiry Date"), default=datetime.date.today)

    class Meta:
        verbose_name = _("Content Expiry")
