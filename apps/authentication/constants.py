import os

SHOPIFY_API_VERSION = "2021-04"


class ShopifyOauth:
    API_KEY = os.environ["SHOPIFY_API_KEY"]
    SECRET_KEY = os.environ["SHOPIFY_API_SECRET_KEY"]
    SCOPES = (
        "read_orders,write_orders,read_customers,write_customers,read_script_tags,write_script_tags"
    )
    ACCESS_MODE = "per_user"
    REDIRECT_ENDPOINT = "/auth2/"
    ACCESS_TOKEN_HEADER = "X-Shopify-Access-Token"
    ACCESS_TOKEN_ENDPOINT = "/admin/oauth/access_token"
    AUTHORIZE_ENDPOINT = "/admin/oauth/authorize"
    SHOP_DETAILS_ENDPOINT = f"/admin/api/{SHOPIFY_API_VERSION}/shop.json"
    SHOPIFY_BASE_API_URL = f"/admin/api/{SHOPIFY_API_VERSION}"


WEBHOOK_TOPICS = [
    "app/uninstalled",
]
