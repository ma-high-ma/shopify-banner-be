from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.banner.constants import BannerStatus
from apps.banner.models import Banner
from apps.website.models import Website


class BannerView(APIView):
    def get(self, request):
        query_params = request.query_params
        subdomain = query_params.get("host")
        website = Website.objects.filter(subdomain=subdomain).first()
        assert website is not None
        banner_obj = Banner.objects.get(website_id=website.id)
        print("banner = ", banner_obj.__dict__)
        data = {
                "status": banner_obj.status,
                "text": banner_obj.text,
                "style": banner_obj.style,
                "pages": banner_obj.pages
            }
        print("data = ", data)
        return Response(status=200, data=data)

    def post(self, request):
        query_params = request.query_params
        website_id = query_params.get("website_id")
        status = query_params.get('status')
        assert status in [BannerStatus.ENABLED, BannerStatus.DISABLED]
        banner_obj = Banner.objects.get(website_id=website_id)
        banner_obj.status = status
        banner_obj.save()
        return Response(status=204)
