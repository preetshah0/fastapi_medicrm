import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, JSON, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.Enum.PlanStatus import PlanStatus
from app.db.database import Base

if TYPE_CHECKING:
    from app.model.Subscription import Subscription


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    monthly_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00"), server_default=text("0.00")
    )
    yearly_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=Decimal("0.00"), server_default=text("0.00")
    )
    tagline: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    modules: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    max_appointments: Mapped[int | None] = mapped_column(nullable=True)
    max_patients: Mapped[int | None] = mapped_column(nullable=True)
    max_staff: Mapped[int | None] = mapped_column(nullable=True)
    max_lab_referrals: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=PlanStatus.DRAFT.value
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )



    subscriptions: Mapped[list["Subscription"]] = relationship(
        "Subscription", back_populates="plan"
    )
