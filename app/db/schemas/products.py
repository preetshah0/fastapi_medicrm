from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    variant: str
    manufacturer: Optional[str] = None
    image: Optional[str] = None
    dosage_strength: Optional[str] = None
    conversion_factor: int
    packs_per_outer: int
    description: Optional[str] = None
    is_available: bool = True


class ProductCreate(ProductBase):
    branch_id: str
    category_id: str
    product_form_id: str
    size_id: str
    outer_size_id: str
    base_unit_id: str
    sku: str
    


class ProductUpdate(BaseModel):
    branch_id: Optional[str] = None
    category_id: Optional[str] = None
    product_form_id: Optional[str] = None
    size_id: Optional[str] = None
    outer_size_id: Optional[str] = None
    base_unit_id: Optional[str] = None
    name: Optional[str] = None
    variant: Optional[str] = None
    sku: Optional[str] = None
    manufacturer: Optional[str] = None
    image: Optional[str] = None
    dosage_strength: Optional[str] = None
    conversion_factor: Optional[int] = None
    packs_per_outer: Optional[int] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None


class ProductResponse(ProductBase):
    id: str
    organization_id: str
    branch_id: str
    category_id: str
    product_form_id: str
    size_id: str
    outer_size_id: str
    base_unit_id: str
    sku: str
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
