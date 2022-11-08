import requests

from apps.authentication.constants import ShopifyOauth


class ShopifyOAuthClient:
    def __init__(self, shop_name: str, access_token: str = ""):
        self.shop_name = shop_name
        self.access_token = access_token

    def get_access_token(self, data):
        res = requests.post(
            f"https://{self.shop_name}{ShopifyOauth.ACCESS_TOKEN_ENDPOINT}",
            data=data,
            timeout=60,
            verify=False
        )
        self.access_token = res.json()["access_token"]
        return self.access_token

    def get_shop_details(self):
        res = requests.get(
            f"https://{self.shop_name}{ShopifyOauth.SHOP_DETAILS_ENDPOINT}",
            headers={ShopifyOauth.ACCESS_TOKEN_HEADER: self.access_token}
        )
        shop_data = res.json()['shop']
        return {
            "name": shop_data['name'],
            "email": shop_data['email'],
            "domain": shop_data['domain'],
            "plan": shop_data['plan_name']
        }

    def build_oauth_redirect_url(self):
        # host = "https://mahima-be.ngrok.io"
        host = "https://mahima-be.app.vtxhub.com"
        redirect_url = (
            f"https://{self.shop_name}{ShopifyOauth.AUTHORIZE_ENDPOINT}?"
            f"client_id={ShopifyOauth.API_KEY}&scope={ShopifyOauth.SCOPES}"
            f"&redirect_uri={host}{ShopifyOauth.REDIRECT_ENDPOINT}"
            f"&grant_options[]={ShopifyOauth.ACCESS_MODE}"
            f"&state=signup"
        )
        return redirect_url
