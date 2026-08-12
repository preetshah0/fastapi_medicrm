import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, Float, Text, Boolean, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.Enum.OrganizationPlanType import OrganizationPlanType
from app.Enum.OrganizationStatus import OrganizationStatus
from app.model.Role import user_roles

if TYPE_CHECKING:
    from app.model.User import User
    from app.model.Role import Roles
    from app.model.Branch import Branch
    from app.model.MedicalRep import MedicalReps
    from app.model.Patient import Patient
    from app.model.ProductCategory import ProductCategory
    from app.model.Product import Product
    from app.model.MasterOption import Master
    from app.model.Inventory import Inventory

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    # --- Info ---
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    ref: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    # phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(Text(), nullable=True)
    profile_photo: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # --- Plan ---
    # plan_id: Mapped[str | None] = mapped_column(
    #     String(36),
    #     ForeignKey("plans.id", ondelete="SET NULL"),
    #     nullable=True
    # )
    # plan_type: Mapped[str] = mapped_column(String(255), nullable = False, server_default=OrganizationPlanType.MONTHLY.value)
    # annual_discount: Mapped[float] = mapped_column(Float, default =0.0, nullable=False)

    # --- Status ---
    status: Mapped[str] = mapped_column(String(255), nullable = False, server_default=OrganizationStatus.ACTIVE.value)
    # --- Timestamps & Soft Delete ---
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # =========================================
    # RELATIONSHIPS
    # =========================================

    # --- belongsTo Plan ---
    # plan: Mapped["Plan"] = relationship(
    #     "Plan",
    #     foreign_keys=[plan_id],
    #     back_populates="organizations"
    # )

    # --- hasMany Users ---
    users: Mapped[list["User"]] = relationship(
        "User",
        foreign_keys="User.organization_id",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # --- hasOne Owner (role=owner) ---
    owner: Mapped["User"] = relationship(
        "User",
        primaryjoin="and_(User.organization_id == Organization.id, User.role == 'owner')",
        foreign_keys="User.organization_id",
        viewonly=True,
        uselist=False
    )

    roles: Mapped[list["Roles"]] = relationship(
        "Roles",
        secondary="join(User, user_roles, User.id == user_roles.c.user_id)",
        primaryjoin="User.organization_id == Organization.id",
        secondaryjoin="Roles.id == user_roles.c.role_id",
        viewonly=True,
    )

    branches: Mapped[list["Branch"]] = relationship(
        "Branch",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    medical_reps: Mapped[list["MedicalReps"]] = relationship(
        "MedicalReps",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # --- hasMany Patients ---
    patients: Mapped[list["Patient"]] = relationship(
        "Patient",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # --- hasMany Product Categories ---
    product_categories: Mapped[list["ProductCategory"]] = relationship(
        "ProductCategory",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # --- hasMany Products ---
    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # --- hasMany Master Options ---
    master_options: Mapped[list["Master"]] = relationship(
        "Master",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # --- hasMany Inventories ---
    inventories: Mapped[list["Inventory"]] = relationship(
        "Inventory",
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    # # --- hasMany Subscriptions ---
    # subscriptions: Mapped[list["Subscription"]] = relationship(
    #     "Subscription",
    #     back_populates="organization",
    #     cascade="all, delete-orphan"
    # )

    # # --- hasOne Active Subscription ---
    # active_subscription: Mapped["Subscription"] = relationship(
    #     "Subscription",
    #     primaryjoin="and_(Subscription.organization_id == Organization.id, Subscription.status == 'active')",
    #     foreign_keys="Subscription.organization_id",
    #     order_by="desc(Subscription.created_at)",
    #     viewonly=True,
    #     uselist=False
    # )

    # # --- hasOne Latest Subscription ---
    # latest_subscription: Mapped["Subscription"] = relationship(
    #     "Subscription",
    #     primaryjoin="Subscription.organization_id == Organization.id",
    #     foreign_keys="Subscription.organization_id",
    #     order_by="desc(Subscription.created_at)",
    #     viewonly=True,
    #     uselist=False,
    #     overlaps="subscriptions,active_subscription"
    # )

    # # =========================================
    # # METHODS (like Laravel's model methods)
    # # =========================================

    # def generate_ref(self) -> str:
    #     """Like Laravel's booted() ref generation"""
    #     import random
    #     import string
    #     return ''.join(random.choices(string.ascii_uppercase, k=8))

    # def has_module(self, module: str) -> bool:
    #     """Like Laravel's hasModule()"""
    #     # RBAC modules always available
    #     if module in ['roles', 'member-permissions']:
    #         return True

    #     active_sub = self.active_subscription
    #     if active_sub and active_sub.features:
    #         return bool(active_sub.get_feature(f"modules.{module}", False))

    #     # Fallback to plan
    #     if self.plan:
    #         return bool(self.plan.modules.get(module, False))

    #     return False

    # def get_feature_limit(self, key: str, default=None):
    #     """Like Laravel's getFeatureLimit()"""
    #     active_sub = self.active_subscription
    #     if active_sub and active_sub.features:
    #         return active_sub.get_feature(f"limits.{key}", default)

    #     if not self.plan:
    #         return default

    #     return getattr(self.plan, key, default)