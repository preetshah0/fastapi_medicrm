from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.products import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.model.Product import Product
from app.model.Branch import Branch
from app.model.ProductCategory import ProductCategory
from app.model.MasterOption import Master
from app.Enum.MasterOptionType import MasterOptionType
from app.Enum.BranchStatus import BranchStatus
from app.owner.controller.product import (
    create_product,
    get_products,
    get_product_by_id,
    update_product,
    delete_product,
)
from app.utils.ApiResponse import success_response, error_response, not_found_response
from app.utils.auth_utils import require_permission

router = APIRouter(prefix="/owner/products", tags=["products"])


@router.post(
    "/create/{organization_id}",
    dependencies=[Depends(require_permission("products", action="create"))],
    response_model=APIResponse[ProductResponse],
)
def create_product_route(
    organization_id: str,
    payload: ProductCreate,
    db: Session = Depends(get_db)
):
    # 1. Validate unique SKU per organization
    existing_sku = db.query(Product).filter(
        Product.organization_id == organization_id,
        Product.sku == payload.sku
    ).first()
    if existing_sku:
        return error_response("This SKU is already in use within your organization.", data="")

    # 2. Validate Branch
    branch = db.query(Branch).filter(
        Branch.id == payload.branch_id,
        Branch.organization_id == organization_id
    ).first()
    if not branch:
        return not_found_response("The selected branch was not found.", data="")
    if hasattr(branch, "status") and str(branch.status).lower() not in ["active", BranchStatus.ACTIVE.value.lower()]:
        return error_response("The selected branch is inactive. Please switch to an active branch.", data="")

    # 3. Validate Category
    category = db.query(ProductCategory).filter(
        ProductCategory.id == payload.category_id,
        ProductCategory.organization_id == organization_id,
        ProductCategory.is_active == True
    ).first()
    if not category:
        return error_response("The selected category is invalid", data="")

    # 4. Validate Master Options (Product Form)
    if payload.product_form_id:
        master_form = db.query(Master).filter(
            Master.id == payload.product_form_id,
            Master.organization_id == organization_id,
            Master.type == MasterOptionType.PRODUCT_FORM.value,
            Master.is_active == True
        ).first()
        if not master_form:
            return error_response("The selected product form is hidden or invalid. Please choose a visible option.", data="")

    # 5. Validate Master Options (Base Unit)
    if payload.base_unit_id:
        master_unit = db.query(Master).filter(
            Master.id == payload.base_unit_id,
            Master.organization_id == organization_id,
            Master.type == MasterOptionType.BASE_UNIT.value,
            Master.is_active == True
        ).first()
        if not master_unit:
            return error_response("The selected unit type is hidden or invalid. Please choose a visible option.", data="")

    # 6. Validate Master Options (SubPack Size)
    if payload.size_id:
        master_size = db.query(Master).filter(
            Master.id == payload.size_id,
            Master.organization_id == organization_id,
            Master.type == MasterOptionType.PRODUCT_SIZE.value,
            Master.is_active == True
        ).first()
        if not master_size:
            return error_response("The selected sub-pack type is hidden or invalid. Please choose a visible option.", data="")

    # 7. Validate Master Options (Outer Pack Size)
    if payload.outer_size_id:
        master_outer = db.query(Master).filter(
            Master.id == payload.outer_size_id,
            Master.organization_id == organization_id,
            Master.type == MasterOptionType.PRODUCT_SIZE.value,
            Master.is_active == True
        ).first()
        if not master_outer:
            return error_response("The selected pack type is hidden or invalid. Please choose a visible option.", data="")

    # 8. Validate low stock threshold
    if payload.low_stock_threshold < 1:
        return error_response("Low stock threshold cannot be less than 1.", data="")

    # Create Product via Controller
    product = create_product(db=db, product_data=payload, organization_id=organization_id)
    return success_response("Product created successfully", product)


@router.get(
    "/organization/{organization_id}",
    dependencies=[Depends(require_permission("products", action="view"))],
    response_model=APIResponse[List[ProductResponse]],
)
def get_products_route(
    organization_id: str,
    branch_id: Optional[str] = None,
    category_id: Optional[str] = None,
    is_available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    products = get_products(
        db=db, 
        organization_id=organization_id, 
        branch_id=branch_id,
        category_id=category_id,
        is_available=is_available, 
        skip=skip, 
        limit=limit
    )
    return success_response("Products fetched successfully", products)


@router.get(
    "/{product_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("products", action="view"))],
    response_model=APIResponse[ProductResponse],
)
def get_product_route(
    product_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    product = get_product_by_id(db=db, product_id=product_id, organization_id=organization_id)
    if not product:
        return not_found_response("Product not found", data="")
    return success_response("Product fetched successfully", product)


@router.put(
    "/{product_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("products", action="edit"))],
    response_model=APIResponse[ProductResponse],
)
def update_product_route(
    product_id: str,
    organization_id: str,
    payload: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = get_product_by_id(db=db, product_id=product_id, organization_id=organization_id)
    if not product:
        return not_found_response("Product not found", data="")

    if payload.low_stock_threshold is not None and payload.low_stock_threshold < 1:
        return error_response("Low stock threshold cannot be less than 1.", data="")

    if payload.sku:
        existing_sku = db.query(Product).filter(
            Product.organization_id == organization_id,
            Product.sku == payload.sku,
            Product.id != product_id
        ).first()
        if existing_sku:
            return error_response("This SKU is already logged in your organization.", data="")

    result = update_product(
        db=db, 
        product_id=product_id, 
        product_data=payload, 
        organization_id=organization_id
    )
    if not result:
        return error_response("Failed to update product", data="")
    return success_response("Product updated successfully", result)


@router.delete(
    "/{product_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("products", action="delete"))],
    response_model=APIResponse[str],
)
def delete_product_route(
    product_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    result = delete_product(db=db, product_id=product_id, organization_id=organization_id)
    if not result:
        return not_found_response("Product not found", data="")
    return success_response("Product deleted successfully", data="")

