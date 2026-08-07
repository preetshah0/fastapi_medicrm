from sqlalchemy.orm import Session
from app.model.ProductCategory import ProductCategory
from app.db.schemas.product_categories import ProductCategoryCreate, ProductCategoryUpdate


def generate_slug(title: str) -> str:
    return title.lower().replace(" ", "-")


def get_product_category_by_slug(db: Session, slug: str) -> ProductCategory | None:
    return db.query(ProductCategory).filter(ProductCategory.slug == slug).first()


def get_product_category_by_id(db: Session, category_id: str) -> ProductCategory | None:
    return db.query(ProductCategory).filter(ProductCategory.id == category_id).first()


def create_product_category(db: Session, product_category: ProductCategoryCreate, organization_id: str) -> ProductCategory | None:
    slug = product_category.slug if product_category.slug else generate_slug(product_category.name)

    existing = get_product_category_by_slug(db, slug)
    if existing:
        return None

    db_product_category = ProductCategory(
        organization_id=organization_id,
        name=product_category.name,
        description=product_category.description,
        slug=slug,
        image=product_category.image,
        is_active=product_category.is_active,
    )
    db.add(db_product_category)
    db.commit()
    db.refresh(db_product_category)
    return db_product_category


def get_product_categories(
    db: Session, 
    organization_id: str, 
    is_active: bool = True,
    skip: int = 0, 
    limit: int = 10
) -> list[ProductCategory]:
    return (
        db.query(ProductCategory)
        .filter(
            ProductCategory.organization_id == organization_id,
            ProductCategory.is_active == is_active
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_product_category(db: Session, category_id: str, payload: ProductCategoryUpdate) -> ProductCategory | None:
    db_category = get_product_category_by_id(db, category_id)
    if not db_category:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if "name" in update_data and "slug" not in update_data:
        new_slug = generate_slug(update_data["name"])
        existing = get_product_category_by_slug(db, new_slug)
        if existing and existing.id != category_id:
            return None
        update_data["slug"] = new_slug

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_product_category(db: Session, category_id: str) -> ProductCategory | None:
    db_category = get_product_category_by_id(db, category_id)
    if not db_category:
        return None

    db.delete(db_category)
    db.commit()
    return db_category