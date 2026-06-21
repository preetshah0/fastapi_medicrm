import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Text, Boolean, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.model.User import User

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    # --- Info ---
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(Text(), nullable=True)
    profile_photo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ref: Mapped[str | None] = mapped_column(String(8), nullable=True)    # like Laravel's ref

    # --- Plan ---
    plan_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("plans.id", ondelete="SET NULL"),
        nullable=True
    )
    plan_type: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=text("'monthly'")
    )
    annual_discount: Mapped[int] = mapped_column(
        nullable=False, server_default=text("0")
    )

    # --- Status ---
    status: Mapped[int] = mapped_column(
        tinyint,                   
        server_default=text("1"),        # 1 = active 
        
        nullable=False
    )
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

    # --- hasMany Branches ---
    # branches: Mapped[list["Branch"]] = relationship(
    #     "Branch",
    #     back_populates="organization",
    #     cascade="all, delete-orphan"
    # )

    # # --- hasMany Patients ---
    # patients: Mapped[list["Patient"]] = relationship(
    #     "Patient",
    #     back_populates="organization",
    #     cascade="all, delete-orphan"
    # )

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