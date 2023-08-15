import pytest
from unittest.mock import MagicMock, patch

from actions.shopify_add_product import ShopifyAddProductTool, ShopifyAddProductSchema
from actions.shopify_list_products import ShopifyListProductsTool, ShopifyListProductsSchema
from actions.shopify_helper import ShopifyHelper


def test_shopify_add_product_schema():
    schema = ShopifyAddProductSchema(
        product_title="Elegant Vase",
        product_description="A beautiful vase for your living room.",
        price=49.99,
    )

    assert schema.product_title == "Elegant Vase"
    assert schema.product_description == "A beautiful vase for your living room."
    assert schema.price == 49.99


@pytest.fixture
def shopify_add_product_tool():
    return ShopifyAddProductTool()


@patch.object(ShopifyHelper, "add_product")
async def test_shopify_add_product_tool_execute(mock_add_product, shopify_add_product_tool):
    shopify_add_product_tool.toolkit_config.get_tool_config = MagicMock(side_effect=["test_token", "test_store_url"])

    # Update the mocked response to include the key "product"
    mock_add_product.return_value = {"product": {"id": 12345, "title": "Elegant Vase"}}

    response = await shopify_add_product_tool._execute(
        product_title="Elegant Vase",
        product_description="A beautiful vase for your living room.",
        price=49.99,
    )

    assert response == "Product added successfully to Shopify store"


def test_shopify_list_products_schema():
    schema = ShopifyListProductsSchema()
    # Since there are no fields for now, we just check the type
    assert isinstance(schema, ShopifyListProductsSchema)


@pytest.fixture
def shopify_list_products_tool():
    return ShopifyListProductsTool()


@patch.object(ShopifyHelper, "list_products")
async def test_shopify_list_products_tool_execute(mock_list_products, shopify_list_products_tool):
    shopify_list_products_tool.toolkit_config.get_tool_config = MagicMock(side_effect=["test_token", "test_store_url"])

    # Mocking the response to return a list of products
    mock_list_products.return_value = [
        {"id": 1, "title": "Elegant Vase"},
        {"id": 2, "title": "Luxury Sofa"}
    ]

    response = await shopify_list_products_tool._execute()

    assert len(response) == 2
    assert response[0]["title"] == "Elegant Vase"
    assert response[1]["title"] == "Luxury Sofa"

    # Testing the error scenario
    mock_list_products.return_value = None

    response = await shopify_list_products_tool._execute()

    assert "Error: Unable to fetch products" in response


async def test_shopify_list_verify():
    token = "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"
    store_url = "https://a6cc66.myshopify.com"
    helper = ShopifyHelper(token, store_url)

    # Fetch the first page of products
    products = await helper.list_products(limit=1)
    print(products)

    # Fetch subsequent pages using page_info
    page_info = helper.get_next_page_info()
    iterations = 0
    while page_info and iterations < 5:
        products = await helper.list_products(limit=1, page_info=page_info)
        print(products)
        page_info = helper.get_next_page_info()
        iterations += 1
