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

        # admin_dashboard_url = f"https://{shop}/admin/apps/testapp/dashboard/"
        # admin_dashboard_url = f"https://mahima-be.ngrok.io/dashboard/"
        admin_dashboard_url = f"https://mahima-fe.app.vtxhub.com/"
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

# def get_shop_details(self, shop, access_token):
#     res = requests.get(
#         f"https://{shop}/admin/api/2021-04/shop.json",
#         headers={"X-Shopify-Access-Token": access_token}
#     )
#     print("shop response = ", res.text)
#     return

# def get_access_token_from_shopify(self, shop, code):
#     data = {
#         "client_id": "2ec348a43d44e5488a22b0cfecee634e",
#         "client_secret": "39813af02d0e80ef8e04f92317b7e0e9",
#         "code": code}
#     res = requests.post(
#         f"https://{shop}/admin/oauth/access_token",
#         data=data,
#         verify=False,
#         timeout=60
#     )
#     """
#     response =  {
#     "access_token":"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",
#     "scope":"write_orders,write_customers,write_products,write_content,write_price_rules,write_themes"}
#     """
#     print("response = ", res.json())
#     return res.json()["access_token"]

# def create_redirect_url(self, shop, absolute_url):
#     SCOPES = (
#         "read_orders,write_orders,read_customers,write_customers,"
#         "read_products,write_products,read_content,write_content,"
#         "read_price_rules,write_price_rules,read_themes,write_themes"
#     )
#     SHOPIFY_API_KEY = "2ec348a43d44e5488a22b0cfecee634e"
#     redirect_url = (
#         f"https://{shop}/admin/oauth/authorize?"
#         f"client_id={SHOPIFY_API_KEY}&scope={SCOPES}"
#         # f"&redirect_uri={host}/account/oauth/shopify/authorize"
#         f"&redirect_uri=https://c9ce4770160f.ngrok.io/auth2/"
#         f"&grant_options[]=per_user"
#         f"&state=signup"
#     )
#     return redirect_url

"""
        {"shop":
        {"id":66971566298,
        "name":"mahima-test-store", <-----
        "email":"mahima061998@gmail.com", <-----
        "domain":"mahima-test-store.myshopify.com", <------
        "province":"Karnataka",
        "country":"IN",
        "address1":"Teacher's Colony",
        "zip":"560034",
        "city":"Bangalore","source":null,"phone":"","latitude":12.9204334,
        "longitude":77.63571390000001,
        "primary_locale":"en","address2":null,
        "created_at":"2022-10-05T00:52:31+05:30","updated_at":"2022-10-05T01:55:55+05:30",
        "country_code":"IN","country_name":"India","currency":"INR",
        "customer_email":"mahima061998@gmail.com",
        "timezone":"(GMT+05:30) Asia\/Calcutta","iana_timezone":"Asia\/Calcutta",
        "shop_owner":"mahima-test-store Admin",
        "money_format":"Rs. {{amount}}","money_with_currency_format":"Rs. {{amount}}",
        "weight_unit":"kg",
        "province_code":"KA","taxes_included":false,
        "auto_configure_tax_inclusivity":null,"tax_shipping":null,
        "county_taxes":true,"plan_display_name":"Developer Preview",
        "plan_name":"partner_test", <----
        "has_discounts":false,"has_gift_cards":false,
        "myshopify_domain":"mahima-test-store.myshopify.com",
        "google_apps_domain":null,"google_apps_login_enabled":null,
        "money_in_emails_format":"Rs. {{amount}}","money_with_currency_in_emails_format":"Rs. {{amount}}",
        "eligible_for_payments":false,"requires_extra_payments_agreement":false,"password_enabled":true,"has_storefront":true,"eligible_for_card_reader_giveaway":false,"finances":true,"primary_location_id":71697334490,"cookie_consent_level":"implicit","visitor_tracking_consent_preference":"allow_all","checkout_api_supported":false,"multi_location_enabled":true,"setup_required":false,"pre_launch_enabled":false,
        "enabled_presentment_currencies":["INR"]}}
        """
