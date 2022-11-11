from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from apps.account.models import Account
from apps.authentication.constants import ShopifyOauth
from apps.authentication.helpers.shopify_client import ShopifyOAuthClient
from apps.authentication.services.script_tag import ScriptTagService
from apps.authentication.services.webhook import WebhookService
from apps.banner.models import Banner
from apps.website.models import Website


class Auth1View(APIView):
    def get(self, request):
        """
        Absolute URL = GET
        http: // mahima-be.ngrok.io / auth1 /?hmac =
        40df291a195f7e898a49fc24e15cd472eaf8f97954dd20c80d75e8133d61f912
        & host = bWFoaW1hLXRlc3Qtc3RvcmUubXlzaG9waWZ5LmNvbS9hZG1pbg
        & shop = mahima-test-store.myshopify.com
        & timestamp = 166491346
        """
        query_params = request.query_params

        shop = query_params.get("shop")
        # absolute_url = request.build_absolute_uri()

        # Todo: Implement verify request hmac

        oauth_client = ShopifyOAuthClient(shop_name=shop)
        redirect_url = oauth_client.build_oauth_redirect_url()
        return redirect(redirect_url)

    """
    https://mahima-test-store.myshopify.com/admin/oauth/request_grant
    ?access_change_uuid=53663542-4e07-4606-a3af-9a746cd54246
    &client_id=2ec348a43d44e5488a22b0cfecee634e <- Your Apps' API Key
    """


class Auth2View(APIView):
    """
    GET /auth2/
    ?code=1c3d2a1e9180d51cd33dd3c473a1a74a
    &hmac=37f02ad83c303f54e7f4cecfcbfc6f35466886ba66941174ce59fb680af54883
    &host=bWFoaW1hLXRlc3Qtc3RvcmUubXlzaG9waWZ5LmNvbS9hZG1pbg
    &shop=mahima-test-store.myshopify.com
    &timestamp=1664952589
    """

    def get(self, request):
        query_params = request.query_params
        shop = query_params.get("shop")
        code = query_params.get("code")
        oauth_client = ShopifyOAuthClient(shop_name=shop)

        access_token = oauth_client.get_access_token(
            data={
                "client_id": ShopifyOauth.API_KEY,
                "client_secret": ShopifyOauth.SECRET_KEY,
                "code": code
            }
        )
        shop_details = oauth_client.get_shop_details()
        account = Account.objects.create(
            name=shop_details["name"],
            email=shop_details["email"],
            status="active"
        )
        website = Website.objects.create(
            account=account,
            subdomain=shop_details["domain"],
            access_token=access_token,
            status="active",
            shopify_plan=shop_details["plan"]
        )

        webhook_service = WebhookService(shop_url=shop_details["domain"])
        webhook_service.add_all()
        script_tag_service = ScriptTagService(subdomain=shop_details["domain"])
        script_tag_service.add()
        banner = Banner.objects.create(website_id=website.id)

        admin_dashboard_url = f"https://mahima-fe.app.vtxhub.com/?website_id={website.id}"
        print("dash url = ", admin_dashboard_url)
        return redirect(admin_dashboard_url)


class DashboardView(APIView):
    def get(self, request):
        print("inside DashboardView = ", request.query_params)
        return Response(status=204)


class WebhookView(APIView):
    def post(self, request):
        print("INSIDE WEBHOOK VIEW body = ", request.data)
        print("INSIDE WEBHOOK VIEW headers = ", request.headers)
        headers = request.headers
        request_body = request.data
        query_params = request.query_params
        # if headers.get("X-Shopify-Topic") == "app/uninstalled":
        if headers.get("X-Shopify-Topic") == "app/uninstalled":
            print("inside uninstalled")
            subdomain = query_params["subdomain"]

            website = Website.objects.filter(subdomain=subdomain).last()
            website.status = "uninstalled"
            website.save()

            script_tag_service = ScriptTagService(subdomain=subdomain)
            script_tag_service.delete_all()
        return Response()


"""----------------------------------------------"""
