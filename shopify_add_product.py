from typing import Type
from pydantic import BaseModel, Field
from shopify_helper import ShopifyHelper
from superagi.tools.base_tool import BaseTool

class ShopifyAddProductSchema(BaseModel):
    product_title: str = Field(
        ...,
        description="Title of the product to be added",
    )
    product_description: str = Field(
        ...,
        description="Description of the product",
    )
    price: float = Field(
        ...,
        description="Price of the product",
    )

class ShopifyAddProductTool(BaseTool):
    """
    Add Product tool for Shopify

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name: str = "Shopify Add Product"
    args_schema: Type[BaseModel] = ShopifyAddProductSchema
    description: str = "Add a product to a Shopify store"
    agent_id: int = None
    agent_execution_id: int = None

    async def _execute(self, product_title: str, product_description: str, price: float) -> str:
        """
        Execute the add product tool for Shopify.

        Args:
            product_title : The title of the product to add.
            product_description : The description of the product.
            price : The price of the product.

        Returns:
            Success message if product is added successfully else error message.
        """
        try:
            shopify_access_token = self.get_tool_config("SHOPIFY_ACCESS_TOKEN")
            shopify_store_url = self.get_tool_config("SHOPIFY_STORE_URL")
            shopify_helper = ShopifyHelper(shopify_access_token, shopify_store_url)
            response = await shopify_helper.add_product(product_title, product_description, price)
            if "product" in response:
                return "Product added successfully to Shopify store"
            else:
                return "Error while adding product."
        except Exception as err:
            return f"Error: Unable to add product to Shopify store {err}"
