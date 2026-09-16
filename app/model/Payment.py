import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Subscription import Subscription


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subscription_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=True, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, default="INR", server_default=text("'INR'")
    )
    # payment_mode: Mapped[str] = mapped_column(
    #     String(50), nullable=False, server_default=text("'manual'")
    # )
    # provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # provider_payment_id: Mapped[str | None] = mapped_column(
    #     String(255), nullable=True, unique=True
    # )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # status: Mapped[str] = mapped_column(
    #     String(50), nullable=False, server_default=text("'pending'")
    # )
    reference_no: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    organization: Mapped["Organization"] = relationship(
        "Organization", back_populates="payments"
    )
    subscription: Mapped["Subscription | None"] = relationship(
        "Subscription", back_populates="payments"
    )
