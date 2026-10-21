from decimal import Decimal
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class PlanBase(BaseModel):
    name: str
    monthly_price: Decimal
    yearly_price: Decimal
    tagline: Optional[str] = None
    modules: dict[str, Any]
    max_appointments: Optional[int] = None
    max_patients: Optional[int] = None
    max_staff: Optional[int] = None
    max_lab_referrals: Optional[int] = None
    stripe_product_id: Optional[str] = None
    stripe_monthly_price_id: Optional[str] = None
    stripe_yearly_price_id: Optional[str] = None

class PlanCreate(PlanBase):
    status: bool = True


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    monthly_price: Optional[Decimal] = None
    yearly_price: Optional[Decimal] = None
    tagline: Optional[str] = None
    modules: Optional[dict[str, Any]] = None
    max_appointments: Optional[int] = None
    max_patients: Optional[int] = None
    max_staff: Optional[int] = None
    max_lab_referrals: Optional[int] = None
    stripe_product_id: Optional[str] = None
    stripe_monthly_price_id: Optional[str] = None
    stripe_yearly_price_id: Optional[str] = None
    status: Optional[bool] = None


class PlanStatusUpdate(BaseModel):
    status: bool


class PlanResponse(PlanBase):
    id: str
    slug: str
    status: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
