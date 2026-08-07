from typing import Optional, List
from sqlalchemy.orm import Session
from app.model.Product import Product
from app.db.schemas.products import ProductCreate, ProductUpdate


def generate_slug(name: str, sku: str) -> str:
    slug_name = name.lower().strip().replace(" ", "-")
    slug_sku = sku.lower().strip().replace(" ", "-")
    return f"{slug_name}-{slug_sku}"


def create_product(db: Session, product_data: ProductCreate, organization_id: str) -> Product:
    slug = generate_slug(product_data.name, product_data.sku)

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
        conversion_factor=product_data.conversion_factor,
        packs_per_outer=product_data.packs_per_outer,
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
    is_available: bool = True,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Product)
        .filter(
            Product.organization_id == organization_id,
            Product.is_available == is_available
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


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