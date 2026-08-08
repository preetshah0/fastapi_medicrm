import uuid
from typing import TYPE_CHECKING
from datetime import datetime, date, time
from sqlalchemy import String, ForeignKey, DateTime, Date, Time, Integer, Float, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from app.db.database import Base
from app.Enum.PatientGender import PatientGender
from app.Enum.PatientBloodGroup import PatientBloodGroup
from app.Enum.PatientVisitPaymentMode import PatientVisitPaymentMode
from app.Enum.PatientVisitPaymentStatus import PatientVisitPaymentStatus
from app.Enum.AppointmentDuration import AppointmentDuration


if TYPE_CHECKING:
    from app.model.User import User
    from app.model.Organization import Organization
    from app.model.Appointment import Appointment

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    # user_id: Mapped[str] = mapped_column(
    #     String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    # )
    
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ref_code: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    
    phone: Mapped[str | None] = mapped_column(String(255), nullable=True)
    age: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    blood_group: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    profile_photo: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    # doctor: Mapped["User"] = relationship("User", back_populates="patients", foreign_keys=[user_id])
    organization: Mapped["Organization"] = relationship("Organization", back_populates="patients")
    reports: Mapped[list["Report"]] = relationship("Report", back_populates="patient", cascade="all, delete-orphan")
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="patient", cascade="all, delete-orphan")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    patient_appointments: Mapped[list["PatientAppointment"]] = relationship("PatientAppointment", back_populates="patient", cascade="all, delete-orphan")
    patient_visits: Mapped[list["PatientVisit"]] = relationship("PatientVisit", back_populates="patient", cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )
    
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    notes: Mapped[str] = mapped_column(Text, nullable=False)
    note_date: Mapped[date] = mapped_column(Date, nullable=True)
    written_by: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="notes")
    user: Mapped["User"] = relationship("User", back_populates="notes", foreign_keys=[user_id])


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )

    report_type: Mapped[str] = mapped_column(String(255), nullable=False)
    attachment: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    report_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    patient: Mapped["Patient"] = relationship("Patient", back_populates="reports")


class PatientAppointment(Base):
    __tablename__ = "patient_appointments"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    appointment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False
    )
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )

    location: Mapped[str] = mapped_column(String(255), nullable=False)
    appointment_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    appointment_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=str(AppointmentDuration.THIRTY.value)
    )

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    appointment: Mapped["Appointment"] = relationship(
        "Appointment", foreign_keys=[appointment_id], back_populates="patient_appointments"
    )
    patient: Mapped["Patient"] = relationship(
        "Patient", foreign_keys=[patient_id], back_populates="patient_appointments"
    )


class PatientVisit(Base):
    __tablename__ = "patient_visits"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    appointment_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("appointments.id", ondelete="CASCADE"), nullable=False
    )
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )

    visited_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    visit_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    amount_charged: Mapped[float | None] = mapped_column(Float, nullable=True)

    payment_mode: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    payment_status: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    appointment: Mapped["Appointment"] = relationship(
        "Appointment", foreign_keys=[appointment_id], back_populates="patient_visits"
    )
    patient: Mapped["Patient"] = relationship(
        "Patient", foreign_keys=[patient_id], back_populates="patient_visits"
    )

