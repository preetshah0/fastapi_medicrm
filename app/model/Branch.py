import uuid
from datetime import datetime, time
from typing import TYPE_CHECKING, Any
from sqlalchemy import String, DateTime, Time, Float, Text, Boolean, text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.Enum.BranchStatus import BranchStatus

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.User import User
    from app.model.Role import Roles
    from app.model.MedicalRep import MedicalReps
    from app.model.Appointment import Appointment
    from app.model.Inventory import Inventory


class BranchUser(Base):
    __tablename__ = "branch_users"

    branch_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("branches.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_roles: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default="active",
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    branch: Mapped["Branch"] = relationship(
        "Branch",
        back_populates="branch_users",
        foreign_keys=[branch_id],
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="branch_users",
        foreign_keys=[user_id],
    )
    role: Mapped["Roles"] = relationship(
        "Roles",
        back_populates="branch_users",
        foreign_keys=[role_id],
    )


class Branch(Base):
    __tablename__ = "branches"

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
    branch_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    branch_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default= BranchStatus.ACTIVE.value
    )
    address: Mapped[str | None] = mapped_column(
        Text(),
        nullable=True
    )

    city: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    state: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    opening_time: Mapped[time] = mapped_column(Time, nullable=False, default=time(9, 0))
    closing_time: Mapped[time] = mapped_column(Time, nullable=False, default=time(18, 0))
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
 

    organization: Mapped["Organization"] = relationship(
        "Organization",
        foreign_keys=[organization_id],
        back_populates="branches",
    )

    branch_users: Mapped[list["BranchUser"]] = relationship(
        "BranchUser",
        back_populates="branch",
        cascade="all, delete-orphan",
    )

    medical_reps: Mapped[list["MedicalReps"]] = relationship(
        "MedicalReps",
        back_populates="branch",
        cascade="all, delete-orphan"
    )

    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="branch",
        cascade="all, delete-orphan"
    )

    inventories: Mapped[list["Inventory"]] = relationship(
        "Inventory",
        back_populates="branch",
        cascade="all, delete-orphan"
    )

    