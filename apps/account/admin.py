from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from apps.account.models import Account


@admin.register(Account)
class AccountAdmin(ModelAdmin):
    list_display = [f.name for f in Account._meta.fields]
