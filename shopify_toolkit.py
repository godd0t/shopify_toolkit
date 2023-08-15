from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit
from shopify_add_product import ShopifyAddProductTool
from tool_config_key_type import ToolConfigKeyType
from tool_configuration import ToolConfiguration


class ShopifyToolkit(BaseToolkit, ABC):
    name: str = "Shopify Toolkit"
    description: str = "Shopify Toolkit contains all Shopify related tools"

    def get_tools(self) -> List[BaseTool]:
        return [ShopifyAddProductTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="SHOPIFY_ACCESS_TOKEN", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=True),
            ToolConfiguration(key="SHOPIFY_STORE_URL", key_type=ToolConfigKeyType.STRING, is_required=True, is_secret=False)
        ]
