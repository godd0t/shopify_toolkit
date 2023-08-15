from typing import Type, List
from pydantic import BaseModel, Field
from actions.shopify_helper import ShopifyHelper
from superagi.tools.base_tool import BaseTool


class ShopifyListProductsSchema(BaseModel):
    limit: int = Field(None, description="Number of results to return per page.")
    collection_id: int = Field(None, description="ID of the collection to filter products by.")
    page_info: str = Field(None, description="Page info for pagination.")


class ShopifyListProductsTool(BaseTool):
    """
    List Products tool for Shopify

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "Shopify List Products"
    args_schema: Type[BaseModel] = ShopifyListProductsSchema
    description: str = "List all products from a Shopify store"
    agent_id: int = None
    agent_execution_id: int = None

    async def _execute(self, limit: int = None, collection_id: int = None, page_info: str = None):
        """
        Execute the list products tool for Shopify.

        Returns:
            List of products if fetched successfully else error message.
        """
        try:
            shopify_access_token = self.get_tool_config("SHOPIFY_ACCESS_TOKEN")
            shopify_store_url = self.get_tool_config("SHOPIFY_STORE_URL")
            shopify_helper = ShopifyHelper(shopify_access_token, shopify_store_url)
            products = await shopify_helper.list_products(limit=limit, collection_id=collection_id, page_info=page_info)
            if products:
                return products
            else:
                return "Error while fetching products."
        except Exception as err:
            return f"Error: Unable to fetch products from Shopify store {err}"
