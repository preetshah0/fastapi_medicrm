import uuid
from typing import TYPE_CHECKING
from datetime import datetime, date, time
from sqlalchemy import String, ForeignKey, DateTime, Date, Time, Integer, Float, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.Enum.AppointmentStatus import AppointmentStatus
from app.Enum.AppointmentType import AppointmentType
from app.Enum.AppointmentDuration import AppointmentDuration
from app.Enum.PatientVisitPaymentMode import PatientVisitPaymentMode
from app.Enum.PatientVisitPaymentStatus import PatientVisitPaymentStatus

if TYPE_CHECKING:
    from app.model.Branch import Branch
    from app.model.User import User
    from app.model.Patient import Patient, PatientAppointment, PatientVisit


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
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

    appointment_date: Mapped[date] = mapped_column(Date, nullable=True)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    end_time: Mapped[time | None] = mapped_column(Time, nullable=True)

    status: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=AppointmentStatus.SCHEDULED.value
    )
    type: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=AppointmentType.GENERAL_CONSULTATION.value
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=str(AppointmentDuration.THIRTY.value)
    )
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Relationships
    branch: Mapped["Branch"] = relationship(
        "Branch", foreign_keys=[branch_id], back_populates="appointments"
    )
    doctor: Mapped["User"] = relationship(
        "User", foreign_keys=[doctor_id], back_populates="doctor_appointments"
    )
    patient: Mapped["Patient"] = relationship(
        "Patient", foreign_keys=[patient_id], back_populates="appointments"
    )

    patient_appointments: Mapped[list["PatientAppointment"]] = relationship(
        "PatientAppointment", back_populates="appointment", cascade="all, delete-orphan"
    )
    patient_visits: Mapped[list["PatientVisit"]] = relationship(
        "PatientVisit", back_populates="appointment", cascade="all, delete-orphan"
    )


