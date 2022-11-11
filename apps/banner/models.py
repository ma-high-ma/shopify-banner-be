from django.contrib.postgres.fields import ArrayField
from django.db import models

from apps.banner.constants import BannerStatus, DEFAULT_STYLE, DEFAULT_TEXT
from apps.website.models import Website


class Banner(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    text = models.CharField(max_length=512, default=DEFAULT_TEXT)
    status = models.CharField(max_length=50, choices=BannerStatus.choices, default=BannerStatus.DISABLED)
    style = models.JSONField(default=DEFAULT_STYLE)
    pages = ArrayField(
        models.CharField(max_length=124, blank=True, null=True),
        default=["all"],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

