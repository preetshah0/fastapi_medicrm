from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.Enum.AutoRenew import AutoRenew
from app.Enum.BillingPeriod import BillingPeriod
from app.Enum.SubscriptionStatus import SubscriptionStatus


class SubscriptionBase(BaseModel):
    plan_id: str
    start_date: datetime
    total_billing_amount: Decimal
    currency: str 
    billing_period: BillingPeriod = BillingPeriod.MONTHLY
    auto_renew: AutoRenew = AutoRenew.ACTIVE
    cancelled_at: Optional[datetime] = None
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    total_billing_amount: Optional[Decimal] = None
    billing_period: Optional[BillingPeriod] = None
    auto_renew: Optional[AutoRenew] = None
    cancelled_at: Optional[datetime] = None
    status: Optional[SubscriptionStatus] = None


class SubscriptionResponse(SubscriptionBase):
    id: str
    organization_id: str
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
