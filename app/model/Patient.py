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
from app.Enum.LabReferralPriority import LabReferralPriority


if TYPE_CHECKING:
    from app.model.User import User
    from app.model.Organization import Organization
    from app.model.Branch import Branch
    from app.model.Laboratory import Laboratory
    from app.model.Appointment import Appointment
    from app.model.Prescription import Prescription
    from app.model.FollowUp import FollowUp
    from app.model.Sale import Sale

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
    prescriptions: Mapped[list["Prescription"]] = relationship("Prescription", back_populates="patient", cascade="all, delete-orphan")
    followups: Mapped[list["FollowUp"]] = relationship("FollowUp", foreign_keys="FollowUp.patient_id", back_populates="patient", cascade="all, delete-orphan")
    sales: Mapped[list["Sale"]] = relationship("Sale", foreign_keys="Sale.patient_id", back_populates="patient", cascade="all, delete-orphan")
    lab_referrals: Mapped[list["PatientLabReferral"]] = relationship("PatientLabReferral", back_populates="patient", cascade="all, delete-orphan")


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
    lab_referrals: Mapped[list["PatientLabReferral"]] = relationship("PatientLabReferral", back_populates="report")


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


class PatientLabReferral(Base):
    __tablename__ = "patient_lab_referrals"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    branch_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False
    )
    doctor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )

    ref_no: Mapped[str] = mapped_column(String(255), nullable=False)
    referred_by: Mapped[str] = mapped_column(String(255), nullable=False)
    clinical_notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    report_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("reports.id", ondelete="SET NULL"), nullable=True
    )
    special_instructions: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lab_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("laboratories.id", ondelete="CASCADE"), nullable=False
    )
    priority: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=LabReferralPriority.LOW.value
    )

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="lab_referrals")
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id], back_populates="lab_referrals")
    doctor: Mapped["User"] = relationship("User", foreign_keys=[doctor_id], back_populates="doctor_lab_referrals")
    patient: Mapped["Patient"] = relationship("Patient", back_populates="lab_referrals")
    report: Mapped["Report | None"] = relationship("Report", back_populates="lab_referrals")
    laboratory: Mapped["Laboratory"] = relationship("Laboratory", foreign_keys=[lab_id], back_populates="lab_referrals")
    tests_required: Mapped[list["TestRequired"]] = relationship("TestRequired", back_populates="referral", cascade="all, delete-orphan")


class TestRequired(Base):
    __tablename__ = "test_required"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    referral_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patient_lab_referrals.id", ondelete="CASCADE"), nullable=False
    )
    test_name: Mapped[str] = mapped_column(String(255), nullable=False)
    test_code: Mapped[str] = mapped_column(String(255), nullable=False)
    test_description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    attachments: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    referral: Mapped["PatientLabReferral"] = relationship("PatientLabReferral", back_populates="tests_required")


