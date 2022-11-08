from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.banner.models import Banner
from apps.website.models import Website


class BannerView(APIView):
    def get(self, request):
        query_params = request.query_params
        subdomain = query_params.get("host")
        website = Website.objects.filter(subdomain=subdomain).first()
        assert website is not None
        banner_obj = Banner.objects.get(website_id=website.id)
        data = {
                "status": banner_obj.status,
                "style": banner_obj.style,
                "pages": banner_obj.pages
            }
        return Response(status=200, data=data)
