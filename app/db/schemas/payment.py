from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from app.Enum.PaymentStatus import PaymentStatus
from app.Enum.PaymentMode import PaymentMode
from app.Enum.PaymentProvider import PaymentProvider


class PaymentBase(BaseModel):
    amount: float
    currency: str = "INR"
    payment_mode: PaymentMode = PaymentMode.GATEWAY
    provider: PaymentProvider = PaymentProvider.STRIPE
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


class AdminPaymentResponse(PaymentResponse):
    organization_name: Optional[str] = None
    organization_ref: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AdminPaymentSummaryResponse(BaseModel):
    total_revenue: float
    currency: str
    total_count: int
    paid_count: int
    failed_count: int
    pending_count: int

    model_config = ConfigDict(from_attributes=True)


class AdminPaymentResponse(PaymentResponse):
    organization_name: Optional[str] = None
    organization_ref: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AdminPaymentSummaryResponse(BaseModel):
    total_revenue: float
    currency: str
    total_count: int
    paid_count: int
    failed_count: int
    pending_count: int

    model_config = ConfigDict(from_attributes=True)
