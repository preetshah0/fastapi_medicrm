import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import text, Boolean, String, ForeignKey, Text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Product import Product


class Master(Base):
    __tablename__ = "master_options"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="master_options")

    product_forms: Mapped[list["Product"]] = relationship("Product", foreign_keys="Product.product_form_id", back_populates="product_form")
    sizes: Mapped[list["Product"]] = relationship("Product", foreign_keys="Product.size_id", back_populates="size")
    outer_sizes: Mapped[list["Product"]] = relationship("Product", foreign_keys="Product.outer_size_id", back_populates="outer_size")
    base_units: Mapped[list["Product"]] = relationship("Product", foreign_keys="Product.base_unit_id", back_populates="base_unit")

    __table_args__ = (
        UniqueConstraint("organization_id", "type", "slug", name="uq_master_options_org_type_slug"),
        Index("idx_master_options_type_active", "type", "is_active"),
    )