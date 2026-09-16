from decimal import Decimal
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.Enum.PlanStatus import PlanStatus


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

class PlanCreate(PlanBase):
    status: PlanStatus = PlanStatus.DRAFT


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
    status: Optional[PlanStatus] = None


class PlanResponse(PlanBase):
    id: str
    slug: str
    status: PlanStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
