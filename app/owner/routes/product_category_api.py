from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.product_categories import (
    ProductCategoryCreate,
    ProductCategoryUpdate,
    ProductCategoryResponse,
)
from app.model.ProductCategory import ProductCategory

from app.owner.controller.product_categories import (
    create_product_category,
    get_product_categories,
    get_product_category_by_id,
    get_product_category_by_slug,
    generate_slug,
    update_product_category,
    delete_product_category,
)
from app.utils.ApiResponse import success_response, error_response, not_found_response

router = APIRouter(prefix="/owner/product-categories", tags=["product-categories"])


@router.get("/organization/{organization_id}", response_model=APIResponse[List[ProductCategoryResponse]])
def get_product_categories_route(
    organization_id: str,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    categories = get_product_categories(
        db=db, 
        organization_id=organization_id, 
        is_active=is_active, 
        skip=skip, 
        limit=limit
    )
    return success_response("Product categories fetched successfully", categories)


@router.get("/{slug}", response_model=APIResponse[ProductCategoryResponse])
def get_product_category_by_slug_route(slug: str, db: Session = Depends(get_db)):
    category = get_product_category_by_slug(db, slug)
    if not category:
        return not_found_response("Product category not found", data="")
    return success_response("Product category fetched successfully", category)


@router.post("/create/{organization_id}", response_model=APIResponse[ProductCategoryResponse])
def create_product_category_route(
    organization_id: str,
    payload: ProductCategoryCreate,
    db: Session = Depends(get_db)
):
    slug = payload.slug if payload.slug else generate_slug(payload.name)
    existing = db.query(ProductCategory).filter(ProductCategory.slug == slug).first()
    if existing:
        return error_response("Product category already exists", data="")

    result = create_product_category(db=db, product_category=payload, organization_id=organization_id)
    if not result:
        return error_response("Failed to create product category", data="")

    return success_response("Product category created successfully", result)


@router.get("/{category_id}", response_model=APIResponse[ProductCategoryResponse])
def get_product_category_route(category_id: str, db: Session = Depends(get_db)):
    category = get_product_category_by_id(db, category_id)
    if not category:
        return not_found_response("Product category not found", data="")
    return success_response("Product category fetched successfully", category)


@router.put("/{category_id}", response_model=APIResponse[ProductCategoryResponse])
def update_product_category_route(
    category_id: str,
    payload: ProductCategoryUpdate,
    db: Session = Depends(get_db)
):
    result = update_product_category(db=db, category_id=category_id, payload=payload)
    if not result:
        return error_response("Failed to update product category or duplicate slug exists", data="")
    return success_response("Product category updated successfully", result)


@router.delete("/{category_id}")
def delete_product_category_route(category_id: str, db: Session = Depends(get_db)):
    result = delete_product_category(db=db, category_id=category_id)
    if not result:
        return not_found_response("Product category not found", data="")
    return success_response("Product category deleted successfully", data="")
