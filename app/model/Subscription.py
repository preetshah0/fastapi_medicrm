import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Enum.BillingPeriod import BillingPeriod
from app.Enum.SubscriptionStatus import SubscriptionStatus
from app.db.database import Base
from app.Enum.AutoRenew import AutoRenew

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Plan import Plan
    from app.model.Payment import Payment


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    plan_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    total_billing_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00"), server_default=text("0.00")
    )
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, default="INR", server_default=text("'INR'")
    )
    billing_period: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=BillingPeriod.MONTHLY.value
    )
    auto_renew: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=AutoRenew.ACTIVE.value
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=SubscriptionStatus.ACTIVE.value
    )
    # provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # provider_subscription_id: Mapped[str | None] = mapped_column(
    #     String(255), nullable=True, unique=True
    # )
    # provider_customer_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    plan: Mapped["Plan"] = relationship("Plan", back_populates="subscriptions")
    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="subscriptions"
    )
    payments: Mapped[list["Payment"]] = relationship(
        "Payment", back_populates="subscription"
    )
