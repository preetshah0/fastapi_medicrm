from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    amount: Decimal
    currency: str
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: str
    organization_id: str
    subscription_id: Optional[str] = None
    reference_no: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
