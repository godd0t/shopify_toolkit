import re

import aiohttp


class ShopifyHelper:
    def __init__(self, shopify_access_token, shopify_store_url):
        """
        Initializes the ShopifyHelper with the provided access token and store URL.

        Args:
            shopify_access_token (str): Personal Shopify access token.
            shopify_store_url (str): Shopify store URL.
        """
        self.shopify_access_token = shopify_access_token
        self.shopify_store_url = shopify_store_url
        self.headers = {
            "X-Shopify-Access-Token": self.shopify_access_token,
        }
        self.last_response_headers = None

    async def list_products(self, limit: int = None, collection_id: int = None, page_info: str = None):
        """
        Fetch all products from the Shopify store.

        Returns:
            List of products.
        """
        endpoint = f"{self.shopify_store_url}/admin/api/2021-04/products.json"
        params = {}
        if limit:
            params["limit"] = limit
        if collection_id:
            params["collection_id"] = collection_id
        if page_info:
            params["page_info"] = page_info
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, params=params, headers=self.headers) as response:
                self.last_response_headers = response.headers  # Store the headers
                if response.ok:
                    data = await response.json()
                    return data.get("products", [])
                else:
                    return None

    def get_next_page_info(self):
        """
        Extracts the page_info for the next page from the Link header.

        Returns:
            str: page_info for the next page or None if not found.
        """
        link_header = self.last_response_headers.get('Link', '')
        next_link_match = re.search(r'<[^>]*page_info=([^&>]+)[^>]*>; rel="next"', link_header)
        return next_link_match.group(1) if next_link_match else None

    async def add_product(self, product_title, product_description, price):
        """
        Adds a product to the Shopify store.

        Args:
            product_title (str): Title of the product.
            product_description (str): Description of the product.
            price (float): Price of the product.

        Returns:
            dict: Response from the Shopify API.
        """
        url = f"{self.shopify_store_url}/admin/products.json"
        data = {
            "product": {
                "title": product_title,
                "body_html": product_description,
                "variants": [{"price": price}]
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=self.headers) as response:
                return await response.json()

    # ... [Add other necessary asynchronous methods for operations like updating products, deleting products, etc.]
