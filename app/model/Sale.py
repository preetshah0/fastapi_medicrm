import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import String, ForeignKey, DateTime, Text, Float, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.Enum.SalesStatus import SalesStatus
from app.Enum.SaleType import SaleType
from app.Enum.SalePaymentStatus import SalePaymentStatus
from app.Enum.SalePaymentMethod import SalePaymentMethod

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Branch import Branch
    from app.model.Patient import Patient
    from app.model.Prescription import Prescription
    from app.model.Product import Product
    from app.model.Inventory import Inventory, Batch


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    branch_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False
    )
    patient_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=True
    )
    prescription_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=True
    )

    invoice_number: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    total_amount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.00, server_default=text("0.00")
    )
    discount_amount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.00, server_default=text("0.00")
    )
    sub_total: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.00, server_default=text("0.00")
    )
    tax_amount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.00, server_default=text("0.00")
    )

    payment_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=SalePaymentStatus.PENDING.value
    )
    payment_method: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=SalePaymentMethod.CASH.value
    )
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    sales_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        server_default=SalesStatus.PENDING.value
    )
    sales_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=SaleType.INTERNAL.value,
        server_default=text(f"'{SaleType.INTERNAL.value}'")
    )

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="sales")
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id], back_populates="sales")
    patient: Mapped[Optional["Patient"]] = relationship("Patient", foreign_keys=[patient_id], back_populates="sales")
    prescription: Mapped[Optional["Prescription"]] = relationship("Prescription", foreign_keys=[prescription_id], back_populates="sales")
    items: Mapped[List["SaleItem"]] = relationship(
        "SaleItem", back_populates="sale", cascade="all, delete-orphan"
    )


class SaleItem(Base):
    __tablename__ = "sales_items"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    sale_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sales.id", ondelete="CASCADE"), nullable=False
    )
    product_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    inventory_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("inventories.id", ondelete="CASCADE"), nullable=True
    )
    inventory_batch_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="CASCADE"), nullable=True
    )

    sale_unit: Mapped[str] = mapped_column(
        String(255), nullable=False, default="unit", server_default=text("'unit'")
    )
    quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    base_unit_quantity: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default=text("0")
    )
    unit_price: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.00, server_default=text("0.00")
    )
    discount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.00, server_default=text("0.00")
    )
    final_amount: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.00, server_default=text("0.00")
    )

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    sale: Mapped["Sale"] = relationship("Sale", back_populates="items", foreign_keys=[sale_id])
    product: Mapped["Product"] = relationship("Product", foreign_keys=[product_id], back_populates="sales_items")
    inventory: Mapped[Optional["Inventory"]] = relationship("Inventory", foreign_keys=[inventory_id], back_populates="sales_items")
    inventory_batch: Mapped[Optional["Batch"]] = relationship("Batch", foreign_keys=[inventory_batch_id], back_populates="sales_items")
