import time
from fastapi import APIRouter, HTTPException, Query
from src.product.utils import get_product_attribute_mapping, get_products
from src.product.schemas import (
    ProductAttrData,
    BulkProductCreate,
    ProductDelete,
    ProductQuery,
    ProductUpdate,
    BulkInsertResponse,
    ProductUpdateResponse,
    ProductDeleteResponse,
    RecommendationsResponse,
)
from src.product.embeddings import (
    delete_all_embeddings_from_elasticsearch,
    delete_embedding_from_elasticsearch,
    fetch_recommendations_from_elasticsearch_based_on_query,
    update_embedding_in_elasticsearch,
    upsert_embeddings_to_elasticsearch,
    delete_embeddings_from_elasticsearch,
    fetch_recommendations_from_elasticsearch,
)

router = APIRouter()

@router.post("/bulk_insert/", response_model=BulkInsertResponse)
async def bulk_insert_products(request: BulkProductCreate):
    """
    Bulk insert products into Elasticsearch.
    """
    # Fetch products from the database
    start_time = time.time()
    products = await get_products(request.codes)
    attribute_mapping = await get_product_attribute_mapping(request.codes)
    delete_all = len(request.codes) == 0
    # Upsert embeddings to Elasticsearch
    await upsert_embeddings_to_elasticsearch(ProductAttrData(products=products, attribute_mapping=attribute_mapping), delete_all)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    return BulkInsertResponse(message="Bulk insert successful")

@router.put("/update_product/", response_model=ProductUpdateResponse)
async def update_product(request: ProductUpdate):
    """
    Update a product's details in Elasticsearch.
    """
    # Fetch existing product
    products = await get_products(request.codes)
    attribute_mapping = await get_product_attribute_mapping(request.codes)
    await update_embedding_in_elasticsearch(ProductAttrData(products=products, attribute_mapping=attribute_mapping))
    return ProductUpdateResponse(message="Product updated successfully")

@router.delete("/delete_product/{product_id}", response_model=ProductDeleteResponse)
async def delete_product(product_id: str):
    """
    Delete a product from Elasticsearch.
    """
    # Delete document from Elasticsearch
    await delete_embedding_from_elasticsearch(product_id)
    return ProductDeleteResponse(message="Product deleted successfully")

@router.delete("/delete_products/", response_model=ProductDeleteResponse)
async def delete_products(request: ProductDelete):
    """
    Delete multiple products from Elasticsearch.
    """
    # Delete documents from Elasticsearch
    await delete_embeddings_from_elasticsearch(request.codes)
    return ProductDeleteResponse(message="Products deleted successfully")

@router.delete("/delete_all_products/", response_model=ProductDeleteResponse)
async def delete_all_products(request: ProductDelete):
    """
    Delete multiple products from Elasticsearch.
    """
    # Delete documents from Elasticsearch
    await delete_all_embeddings_from_elasticsearch()
    return ProductDeleteResponse(message="Products deleted successfully")


@router.get("/recommendations/{product_id}", response_model=RecommendationsResponse)
async def get_recommendations(product_id: str, top_k: int = Query(5, ge=1)):
    """
    Fetch product recommendations based on a product ID.
    """
    recommendations = await fetch_recommendations_from_elasticsearch(product_id, top_k)
    return RecommendationsResponse(recommendations=recommendations)

@router.post("/recommendations/query/", response_model=RecommendationsResponse)
async def get_recommendations_by_query(request: ProductQuery):
    """
    Fetch product recommendations based on a query.
    """
    recommendations = await fetch_recommendations_from_elasticsearch_based_on_query(request.query)
    return RecommendationsResponse(recommendations=recommendations)