from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.Enum.BillingPeriod import BillingPeriod


class StripeCustomerCreate(BaseModel):
    name: str
    email: str
    metadata: Optional[Dict[str, Any]] = None


class StripeProductCreate(BaseModel):
    name: str
    active: bool = True
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class StripeProductUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


# Backward compatibility alias
StripeProduct = StripeProductCreate


class StripePriceCreate(BaseModel):
    product_id: str
    amount_in_cents: int
    currency: str = "usd"
    interval: str
    metadata: Optional[Dict[str, Any]] = None


class StripePriceUpdate(BaseModel):
    active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class StripeCheckoutSessionCreate(BaseModel):
    customer_id: str
    price_id: str
    success_url: str
    cancel_url: str
    metadata: Optional[Dict[str, Any]] = None


class StripeCheckoutRequest(BaseModel):
    plan_id: str
    billing_period: BillingPeriod = BillingPeriod.MONTHLY
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None


class StripeCheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class StripePortalCreate(BaseModel):
    customer_id: str
    return_url: str


class StripePortalRequest(BaseModel):
    return_url: Optional[str] = None


class StripePortalResponse(BaseModel):
    portal_url: str


class StripeCancelSubscriptionRequest(BaseModel):
    subscription_id: str
    at_period_end: bool = False


class StripeSubscriptionStatusResponse(BaseModel):
    subscription_id: str
    status: str
    cancel_at_period_end: bool
    current_period_end: Optional[int] = None


class StripeWebhookVerifyRequest(BaseModel):
    payload: bytes
    sig_header: str
