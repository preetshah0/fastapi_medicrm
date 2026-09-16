import uuid
from typing import TYPE_CHECKING, Optional
from datetime import datetime, date, time
from sqlalchemy import String, ForeignKey, DateTime, Date, Time, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.Enum.FollowupStatus import FollowupStatus
from app.Enum.FollowupVisitStatus import FollowupVisitStatus

if TYPE_CHECKING:
    from app.model.Branch import Branch
    from app.model.Patient import Patient
    from app.model.User import User
    from app.model.Prescription import Prescription
    from app.model.Appointment import Appointment
    from app.model.Organization import Organization


class FollowUp(Base):
    __tablename__ = "followups"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    branch_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("branches.id", ondelete="CASCADE"), nullable=False
    )
    patient_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False
    )
    doctor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    appointment_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("appointments.id", ondelete="CASCADE"), nullable=True
    )
    prescription_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=True
    )

    # Polymorphic discriminator column
    followable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    followable_id: Mapped[str] = mapped_column(String(36), nullable=False)

    followup_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    followup_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    followup_duration: Mapped[int] = mapped_column(Integer, nullable=False, server_default="30")
    status: Mapped[str] = mapped_column(String(50), nullable=False, server_default=FollowupStatus.SCHEDULED.value)
    visited_status: Mapped[str] = mapped_column(String(50), nullable=False, server_default=FollowupVisitStatus.PENDING.value)
    contacted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # Base Relationships with back_populates
    organization: Mapped["Organization"] = relationship("Organization", foreign_keys=[organization_id], back_populates="followups")
    branch: Mapped["Branch"] = relationship("Branch", foreign_keys=[branch_id], back_populates="followups")
    patient: Mapped["Patient"] = relationship("Patient", foreign_keys=[patient_id], back_populates="followups")
    doctor: Mapped["User"] = relationship("User", foreign_keys=[doctor_id], back_populates="doctor_followups")

    __mapper_args__ = {
        "polymorphic_on": followable_type,
        "polymorphic_identity": "followup",
    }


class PrescriptionFollowUp(FollowUp):
    __mapper_args__ = {
        "polymorphic_identity": "prescription",
    }
    prescription: Mapped[Optional["Prescription"]] = relationship(
        "Prescription", foreign_keys=[FollowUp.prescription_id], back_populates="followup"
    )


class AppointmentFollowUp(FollowUp):
    __mapper_args__ = {
        "polymorphic_identity": "appointment",
    }
    appointment: Mapped[Optional["Appointment"]] = relationship(
        "Appointment", foreign_keys=[FollowUp.appointment_id], back_populates="followup"
    )
