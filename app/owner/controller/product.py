from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from decimal import Decimal
from app.model.Product import Product
from app.Enum.MasterOptionType import MasterOptionType
from app.owner.controller.masteroption import get_master_option_dropdown
from app.db.schemas.products import (
    ProductCreate, 
    ProductUpdate,
    ProductPackagingSummaryResponse,
)
from app.db.schemas.master_options import MasterOptionDropdownResponse
from app.services.product_service import (
    calculate_unit_quantities,
    calculate_tier_selling_prices,
)
def get_product_form_dropdown(db: Session, organization_id: str):
    return get_master_option_dropdown(db, organization_id, MasterOptionType.PRODUCT_FORM)


def get_base_unit_dropdown(db: Session, organization_id: str):
    return get_master_option_dropdown(db, organization_id, MasterOptionType.BASE_UNIT)


def get_product_size_dropdown(db: Session, organization_id: str):
    return get_master_option_dropdown(db, organization_id, MasterOptionType.PRODUCT_SIZE)


def generate_slug(name: str, sku: str) -> str:
    slug_name = name.lower().strip().replace(" ", "-")
    slug_sku = sku.lower().strip().replace(" ", "-")
    return f"{slug_name}-{slug_sku}"


def create_product(db: Session, product_data: ProductCreate, organization_id: str) -> Product:
    slug = generate_slug(product_data.name, product_data.sku)

    # Ensure packaging conversion metrics default to minimum 1
    conversion_factor = max(1, product_data.conversion_factor or 1)
    packs_per_outer = max(1, product_data.packs_per_outer or 1)

    db_product = Product(
        organization_id=organization_id,
        branch_id=product_data.branch_id,
        category_id=product_data.category_id,
        product_form_id=product_data.product_form_id,
        size_id=product_data.size_id,
        outer_size_id=product_data.outer_size_id,
        base_unit_id=product_data.base_unit_id,
        name=product_data.name,
        slug=slug,
        variant=product_data.variant,
        sku=product_data.sku,
        manufacturer=product_data.manufacturer,
        image=product_data.image,
        dosage_strength=product_data.dosage_strength,
        conversion_factor=conversion_factor,
        packs_per_outer=packs_per_outer,
        low_stock_threshold=product_data.low_stock_threshold,
        description=product_data.description,
        is_available=product_data.is_available,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(
    db: Session, 
    organization_id: str, 
    branch_id: Optional[str] = None,
    category_id: Optional[str] = None,
    is_available: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Product).filter(Product.organization_id == organization_id)

    if branch_id:
        query = query.filter(Product.branch_id == branch_id)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if is_available is not None:
        query = query.filter(Product.is_available == is_available)

    return query.offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: str, organization_id: str):
    return db.query(Product).filter(
        Product.id == product_id,
        Product.organization_id == organization_id
    ).first()


def update_product(
    db: Session, 
    product_id: str, 
    product_data: ProductUpdate, 
    organization_id: str
):
    product = get_product_by_id(db, product_id, organization_id)


    update_dict = product_data.model_dump(exclude_unset=True)

    if "conversion_factor" in update_dict and update_dict["conversion_factor"] is not None:
        update_dict["conversion_factor"] = max(1, update_dict["conversion_factor"])

    if "packs_per_outer" in update_dict and update_dict["packs_per_outer"] is not None:
        update_dict["packs_per_outer"] = max(1, update_dict["packs_per_outer"])

    if "name" in update_dict or "sku" in update_dict:
        name = update_dict.get("name", product.name)
        sku = update_dict.get("sku", product.sku)
        update_dict["slug"] = generate_slug(name, sku)

    for key, value in update_dict.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: str, organization_id: str) -> bool:
    product = get_product_by_id(db, product_id, organization_id)
    if not product:
        return False

    db.delete(product)
    db.commit()
    return True


def get_product_packaging_summary(product: Product, base_unit_sp: Optional[Decimal] = None) -> ProductPackagingSummaryResponse:
    quantities = calculate_unit_quantities(
        initial_outer_qty=1,
        packs_per_outer=product.packs_per_outer,
        conversion_factor=product.conversion_factor
    )

    prices = None
    if base_unit_sp is not None:
        prices = calculate_tier_selling_prices(
            base_unit_sp=base_unit_sp,
            conversion_factor=product.conversion_factor,
            packs_per_outer=product.packs_per_outer
        )

    summary = ProductPackagingSummaryResponse(
        subpacks_per_box=quantities.subpack_qty,
        base_units_per_box=quantities.base_unit_qty,
        price_tiers=prices
    )
    return summary