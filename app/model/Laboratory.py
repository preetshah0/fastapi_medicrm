import uuid
from datetime import datetime, date, time
from sqlalchemy import String, ForeignKey, text, DateTime, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List, Optional
from app.db.database import Base

from app.Enum.LaboratoryFacilityType import LaboratoryFacilityType
from app.Enum.LaboratoryLabType import LaboratoryLabType
from app.Enum.LaboratoryStatus import LaboratoryStatus

if TYPE_CHECKING:
    from app.model.Organization import Organization
    from app.model.Branch import Branch
    from app.model.MasterOption import Master
    from app.model.Patient import PatientLabReferral

class Laboratory(Base):
    __tablename__ = "laboratories"

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
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    contact_person: Mapped[str] = mapped_column(String(255), nullable=True)
    facility_type: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=LaboratoryFacilityType.INTERNAL.value
    )
    lab_type: Mapped[str] = mapped_column(String(255),nullable=True)
    lab_type_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("master_options.id", ondelete="SET NULL"),
        nullable=False
    )
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    city: Mapped[str] = mapped_column(String(255), nullable=True)
    pincode: Mapped[str] = mapped_column(String(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=LaboratoryStatus.ACTIVE.value
    )
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id])
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id])
    master_lab_type: Mapped[Optional["Master"]] = relationship("Master", foreign_keys=[lab_type_id], back_populates="laboratories")
    visits: Mapped[List["LabVisit"]] = relationship("LabVisit", back_populates="laboratory", cascade="all, delete-orphan")
    lab_referrals: Mapped[List["PatientLabReferral"]] = relationship("PatientLabReferral", foreign_keys="PatientLabReferral.lab_id", back_populates="laboratory", cascade="all, delete-orphan")


class LabVisit(Base):
    __tablename__ = 'lab_visits'

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    lab_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("laboratories.id", ondelete="CASCADE"),
        nullable=False
    )
    visited_date: Mapped[date] = mapped_column(Date, nullable=True)
    visit_time: Mapped[time] = mapped_column(Time, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    speciality: Mapped[str] = mapped_column(String(255), nullable=True)
    from_facility: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    laboratory: Mapped["Laboratory"] = relationship("Laboratory", back_populates="visits")
