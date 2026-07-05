import uuid
from datetime import datetime, date
from sqlalchemy import String, ForeignKey, text, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List
from app.db.database import Base
from app.Enum.SupplierVisitPurpose import SupplierVisitPurpose
from app.Enum.SupplierType import SupplierType

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Branch import Branch
    from app.model.medical_reps import MedicalReps

class Supplier(Base):
    __tablename__  = "suppliers"

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
    type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=SupplierType.DIRECT_SUPPLIER.value
    )
    reps_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("medical_representatives.id", ondelete="CASCADE"),
        nullable=True
    )
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id])
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id])
    medical_rep: Mapped["MedicalReps"] = relationship("MedicalReps", foreign_keys=[reps_id])
    visits: Mapped[List["SupplierVisit"]] = relationship("SupplierVisit", back_populates="supplier", cascade="all, delete-orphan")


class SupplierVisit(Base):
    __tablename__ = 'supplier_visits'

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    supplier_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("suppliers.id", ondelete="CASCADE"),
        nullable=False
    )
    supplier_name: Mapped[str] = mapped_column(String(255), nullable=True)
    visited_date: Mapped[date] = mapped_column(Date, server_default=text("CURRENT_DATE"))
    batch_number: Mapped[str] = mapped_column(String(255), nullable=True)
    visit_purpose: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        server_default=SupplierVisitPurpose.Delivery.value
    )
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="visits")
