from django.contrib import admin

# Register your models here.
from apps.banner.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Banner._meta.fields]
