import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.database import Base
from app.Enum.MRVisitPurpose import MRVisitPurpose

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Branch import Branch

class MedicalReps(Base):
    __tablename__  = "medical_representatives"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    organization_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )
    branch_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("branches.id", ondelete="CASCADE"),
        nullable=False
    )
    reps_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    reps_email: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    reps_phone: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    notes: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    reps_profile_photo: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    company_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    city: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        foreign_keys=[organization_id],
        back_populates="medical_reps",
    )

    branch: Mapped["Branch"] = relationship(
        "Branch",
        foreign_keys=[branch_id],
        back_populates="medical_reps",
    )


class MedicalRepVisit(Base):
    __tablename__ = 'mr_visits'

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    reps_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("medical_representatives.id", ondelete="CASCADE"),
        nullable=False
    )

    visited_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    visit_purpose: Mapped[str] = mapped_column(String(255), nullable=False, server_default=MRVisitPurpose.Other.value)

    product: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )