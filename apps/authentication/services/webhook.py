from urllib.parse import urlencode

import requests

from apps.authentication.constants import SHOPIFY_API_VERSION, ShopifyOauth, WEBHOOK_TOPICS
from apps.website.models import Website


class WebhookService:
    def __init__(self, shop_url):
        self.subdomain = shop_url
        self.shop_url = shop_url
        self.website = Website.objects.filter(subdomain=shop_url).last()
        # self.shop_url = f"https://{self.subdomain}.myshopify.com"
        self.shopify_api_base_url = f"https://{self.shop_url}{ShopifyOauth.SHOPIFY_BASE_API_URL}"

    def _get_headers(self):
        if self.website:
            access_token = self.website.access_token
            # config_api_service = ConfigAPIService(self.website.get('id'))
            # access_token = config_api_service.get(key=ACCESS_TOKEN).get('value').get('value')

            return {
                'x-shopify-access-token': access_token,
                'content-type': "application/json"
            }

    def add_webhooks(self, payload):
        url = f"{self.shopify_api_base_url}/webhooks.json"
        response = requests.post(url=url, json=payload, headers=self._get_headers())
        return response

    def get_all_webhooks(self):
        url = f"{self.shopify_api_base_url}/webhooks.json"
        response = requests.get(url=url, headers=self._get_headers())
        return response

    def add_by_topic(self, topic):
        query_params = {
            "subdomain": self.subdomain,
            "topic": topic
        }
        webhook_endpoint = f"https://mahima-be.app.vtxhub.com/webhooks/?{urlencode(query_params)}"

        payload = {
            "webhook": {
                "topic": topic,
                "address": webhook_endpoint,
                "format": 'json'
            }
        }
        print(payload)
        response = self.add_webhooks(payload=payload)
        print("webhook response = ", response)
        if response.ok:
            return True
        # logger.error(f"Unable to register {topic} webhook on Shopify for subdomain: {self.subdomain}")
        return False

    def add_all(self):
        for topic in WEBHOOK_TOPICS:
            print("topic = ", topic)
            self.add_by_topic(topic)
