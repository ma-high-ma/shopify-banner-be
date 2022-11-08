import requests

from apps.authentication.constants import ShopifyOauth
from apps.website.models import Website


class ScriptTagService:
    def __init__(self, subdomain):
        self.subdomain = subdomain
        self.website = Website.objects.filter(subdomain=subdomain).last()
        self.shopify_api_base_url = f"https://{self.subdomain}{ShopifyOauth.SHOPIFY_BASE_API_URL}"

    def _get_headers(self):
        if self.website:
            access_token = self.website.access_token

            return {
                'x-shopify-access-token': access_token,
                'content-type': "application/json"
            }

    def get_all(self):
        url = f"{self.shopify_api_base_url}/script_tags.json"
        response = requests.get(url=url, headers=self._get_headers())
        if response.ok:
            script_tags = response.json().get('script_tags')
            return script_tags
        return []


    def add(self):
        payload = {
            "script_tag": {
                "event": "onload",
                "display_scope": "all",
                # "src": "https://drive.google.com/uc?id=1xd7IKlDEuhylHf7Eo2RfKeMZ7tBYux9H"
                "src": "https://mahima-test-bucket.s3.amazonaws.com/custom-js.js"
            }
        }
        url = f"{self.shopify_api_base_url}/script_tags.json"
        response = requests.post(url=url, headers=self._get_headers(), json=payload)
        if response.ok:
            print("script tag ADDED!!")
            return True
        print(f"Unable to add script tags on Shopify for subdomain: {self.subdomain}")
        return False

    def delete(self, script_tag_id):
        url = f'{self.shopify_api_base_url}/script_tags/{script_tag_id}.json'
        response = requests.delete(url=url, headers=self._get_headers())
        if response.ok:
            return True
        print(f"Unable to delete script tag {script_tag_id} on Shopify for subdomain: {self.subdomain}")
        return False

    def delete_all(self):
        script_tags = self.get_all()
        for script_tag in script_tags:
            self.delete(script_tag.get("id"))

    def reset(self):
        self.delete_all()
        return self.add()

