from tortoise.exceptions import DoesNotExist

from src.product.models import ProductAttributeModel, ProductModel

async def get_products(product_codes: list[str]) -> list[ProductModel]:
    """
    Get products from the database.
    """
    if not product_codes:
        return await ProductModel.all()

    return await ProductModel.filter(code__in=product_codes)

async def get_product_attribute_mapping(product_code: list[str]) -> dict:
    """
    Get product attribute mapping from the database.
    """
    attributes = await ProductAttributeModel.filter(product_code__in=product_code)
    attribute_mapping = dict[str, list[ProductAttributeModel]]()
    for attr in attributes:
        attribute_mapping.setdefault(attr.product_code, []).append(attr)
    return attribute_mapping

async def get_text_for_embedding(product: ProductModel, attrs: list[ProductAttributeModel]) -> str:
    """
    Get text fields for generating embeddings.
    """
    
    product_text = product.get_text_for_embedding()
    attr_text = " ".join([attr.get_text_for_embedding() for attr in attrs])
    return f"{product_text} {attr_text}"