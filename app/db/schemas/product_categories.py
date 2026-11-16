from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class ProductCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: bool = True


class ProductCategoryCreate(ProductCategoryBase):
    slug: Optional[str] = None


class ProductCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None


class ProductCategoryResponse(ProductCategoryBase):
    id: str
    slug: str
    organization_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
