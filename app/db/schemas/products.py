from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    name: str
    variant: str
    manufacturer: Optional[str] = None
    image: Optional[str] = None
    dosage_strength: Optional[str] = None
    conversion_factor: int
    packs_per_outer: int
    low_stock_threshold: int = Field(default=1, gt=0)
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
    low_stock_threshold: Optional[int] = Field(default=None, gt=0)
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



class ProductUnitQuantitiesResponse(BaseModel):
    subpack_qty: int
    base_unit_qty: int


class ProductTierPricesResponse(BaseModel):
    subpack_sp: Decimal
    pack_sp: Decimal


class SuggestedBatchPricingResponse(BaseModel):
    total_subpacks: int
    total_base_units: int
    base_unit_cost: Decimal
    subpack_cost: Decimal
    pack_cost: Decimal


class ProductPackagingSummaryResponse(BaseModel):
    subpacks_per_box: int
    base_units_per_box: int
    price_tiers: Optional[ProductTierPricesResponse] = None
