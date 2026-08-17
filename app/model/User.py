import uuid
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.Enum.UserRole import UserRole
from app.Enum.UserStatus import UserStatus

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Branch import BranchUser
    from app.model.Patient import Patient, Note
    from app.model.Appointment import Appointment
    from app.model.Role import Roles
    from app.model.UserRefreshToken import UserRefreshToken
    from app.model.Prescription import Prescription

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4())
    )
    
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    # email_verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(255),nullable=False)
    status: Mapped[str] = mapped_column(String(255),nullable = False,server_default=UserStatus.ACTIVE.value)
    
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    profile_photo: Mapped[str | None] = mapped_column(String(255), nullable=True)

    organization_id: Mapped[str | None] = mapped_column(
        String(36), 
        ForeignKey("organizations.id", ondelete="SET NULL"), 
        nullable=True
    )

    # Timestamps & Soft Delete
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="users")
    refresh_tokens: Mapped[list["UserRefreshToken"]] = relationship(
        "UserRefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    roles: Mapped[list["Roles"]] = relationship(
        "Roles",
        secondary="user_roles",
        back_populates="users",
    )

    branch_users: Mapped[list["BranchUser"]] = relationship(
        "BranchUser",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # patients: Mapped[list["Patient"]] = relationship(
    #     "Patient",
    #     back_populates="doctor",
    #     foreign_keys="Patient.user_id",
    #     cascade="all, delete-orphan",
    # )

    notes: Mapped[list["Note"]] = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    doctor_appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment",
        back_populates="doctor",
        foreign_keys="Appointment.doctor_id",
        cascade="all, delete-orphan",
    )

    prescriptions: Mapped[list["Prescription"]] = relationship(
        "Prescription",
        back_populates="doctor",
        foreign_keys="Prescription.doctor_id",
        cascade="all, delete-orphan",
    )