import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import text, Boolean, String, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Branch import Branch
    from app.model.ProductCategory import ProductCategory
    from app.model.MasterOption import Master
    from app.model.Inventory import Inventory, Batch


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    branch_id: Mapped[str] = mapped_column(String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("product_categories.id", ondelete="SET NULL"), nullable=True)
    product_form_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("master_options.id", ondelete="SET NULL"), nullable=True)
    size_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("master_options.id", ondelete="SET NULL"), nullable=True)
    outer_size_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("master_options.id", ondelete="SET NULL"), nullable=True)
    base_unit_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("master_options.id", ondelete="SET NULL"), nullable=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    variant: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sku: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    dosage_strength: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    conversion_factor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    packs_per_outer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default=text("1"))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="products")
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id])
    category: Mapped[Optional["ProductCategory"]] = relationship("ProductCategory", foreign_keys=[category_id], back_populates="products")
    product_form: Mapped[Optional["Master"]] = relationship("Master", foreign_keys=[product_form_id], back_populates="product_forms")
    size: Mapped[Optional["Master"]] = relationship("Master", foreign_keys=[size_id], back_populates="sizes")
    outer_size: Mapped[Optional["Master"]] = relationship("Master", foreign_keys=[outer_size_id], back_populates="outer_sizes")
    base_unit: Mapped[Optional["Master"]] = relationship("Master", foreign_keys=[base_unit_id], back_populates="base_units")

    inventory: Mapped[Optional["Inventory"]] = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete-orphan")
    batches: Mapped[list["Batch"]] = relationship("Batch", back_populates="product", cascade="all, delete-orphan")
