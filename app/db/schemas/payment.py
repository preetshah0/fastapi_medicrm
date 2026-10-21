from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from app.Enum.PaymentStatus import PaymentStatus


class PaymentBase(BaseModel):
    amount: Decimal
    currency: str = "INR"
    payment_mode: str = "gateway"
    provider: str = "stripe"
    provider_payment_id: Optional[str] = None
    provider_invoice_id: Optional[str] = None
    status: PaymentStatus = PaymentStatus.PENDING
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    organization_id: str
    subscription_id: Optional[str] = None
    reference_no: str


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None
    provider_payment_id: Optional[str] = None
    provider_invoice_id: Optional[str] = None
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
