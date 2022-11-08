from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from apps.website.models import Website


@admin.register(Website)
class AccountAdmin(ModelAdmin):
    list_display = [f.name for f in Website._meta.fields]
