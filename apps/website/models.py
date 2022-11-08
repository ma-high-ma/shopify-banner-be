from django.db import models


# Create your models here.
from apps.account.models import Account


class Website(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    subdomain = models.CharField(max_length=512)
    access_token = models.CharField(max_length=512)
    status = models.CharField(max_length=64)
    shopify_plan = models.CharField(max_length=64)
    uninstalled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
