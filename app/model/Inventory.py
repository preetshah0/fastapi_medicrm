import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import String, ForeignKey, Integer, Numeric, Boolean, Date, text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.Enum.InventoryStatus import InventoryStatus
from app.Enum.BatchStatus import BatchStatus

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Branch import Branch
    from app.model.Product import Product
    from app.model.Supplier import Supplier


class Inventory(Base):
    __tablename__ = "inventories"

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
    product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    low_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=10,
        server_default=text("10")
    )
    total_qty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default=text("0")
    )
    inventory_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=InventoryStatus.IN_STOCK.value,
        server_default=text("'in_stock'")
    )
    # total_expired_batches: Mapped[int] = mapped_column(
    #     Integer,
    #     nullable=False,
    #     default=0,
    #     server_default=text("0")
    # )
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="inventories")
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id], back_populates="inventories")
    product: Mapped["Product"] = relationship("Product", foreign_keys=[product_id], back_populates="inventory")
    batches: Mapped[List["Batch"]] = relationship("Batch", foreign_keys="[Batch.inventory_id]", back_populates="inventory", cascade="all, delete-orphan")
    


class Batch(Base):
    __tablename__ = "batches"
    __table_args__ = (
        UniqueConstraint("inventory_id", "batch_no", name="unique_inventory_batch_no"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    inventory_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("inventories.id", ondelete="CASCADE"),
        nullable=False
    )
    product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    supplier_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("suppliers.id", ondelete="SET NULL"),
        nullable=False
    )
    batch_no: Mapped[str] = mapped_column(String(255), nullable=False)
    mfg_date: Mapped[date] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Quantities
    initial_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    current_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    subpack_qty: Mapped[int] = mapped_column(Integer, nullable=False)
    base_unit_qty: Mapped[int] = mapped_column(Integer, nullable=False)

    # Pricing Tiers
    batch_cost_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    mrp: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    batch_selling_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    base_unit_sp: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    subpack_sp: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    pack_sp: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # Status Flags
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=text("1"))
    batch_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=BatchStatus.IN_STOCK.value,
        server_default=text("'in_stock'")
    )

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Relationships
    inventory: Mapped["Inventory"] = relationship("Inventory", foreign_keys=[inventory_id], back_populates="batches")
    product: Mapped["Product"] = relationship("Product", foreign_keys=[product_id], back_populates="batches")
    supplier: Mapped["Supplier"] = relationship("Supplier", foreign_keys=[supplier_id], back_populates="batches")
