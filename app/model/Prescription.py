from typing_extensions import Optional
import uuid
from typing import TYPE_CHECKING
from datetime import datetime, date, time
from decimal import Decimal
from sqlalchemy import String, ForeignKey, DateTime, Date, Time, Text, Boolean, Numeric, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.Enum.PrescriptionStatus import PrescriptionStatus

if TYPE_CHECKING:
    from app.model.Branch import Branch
    from app.model.Patient import Patient
    from app.model.User import User
    from app.model.Inventory import Inventory, Batch
    from app.model.FollowUp import FollowUp
    from app.model.Sale import Sale


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
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

    ref: Mapped[str] = mapped_column(String(8), nullable=False)
    diagnosis: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=PrescriptionStatus.DRAFT.value)
    # pharmacy_status: Mapped[str] = mapped_column(String(255), nullable=False, server_default="pending")
    # amount_to_pay: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default="0.00")
    # payment_method: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # payment_status: Mapped[str] = mapped_column(String(255), nullable=False, server_default="pending")

    follow_up_required: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("0"))
    follow_up_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    follow_up_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    follow_up_note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    followup_duration: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    branch: Mapped["Branch"] = relationship("Branch", back_populates="prescriptions", foreign_keys=[branch_id])
    patient: Mapped["Patient"] = relationship("Patient", back_populates="prescriptions", foreign_keys=[patient_id])
    doctor: Mapped["User"] = relationship("User", back_populates="prescriptions", foreign_keys=[doctor_id])
    medications: Mapped[list["PrescriptionMedication"]] = relationship(
        "PrescriptionMedication",
        back_populates="prescription",
        cascade="all, delete-orphan",
    )
    followup: Mapped[Optional["FollowUp"]] = relationship(
        "PrescriptionFollowUp",
        primaryjoin="Prescription.id == PrescriptionFollowUp.prescription_id",
        back_populates="prescription",
        uselist=False,
        order_by="desc(PrescriptionFollowUp.created_at)",
    )
    sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="prescription")


class PrescriptionMedication(Base):
    __tablename__ = "prescription_medications"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    prescription_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("prescriptions.id", ondelete="CASCADE"), nullable=False
    )
    inventory_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("inventories.id", ondelete="SET NULL"), nullable=True
    )
    inventory_batch_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("batches.id", ondelete="SET NULL"), nullable=True
    )

    drug_name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    dosage: Mapped[str | None] = mapped_column(String(255), nullable=True)
    frequency: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meal_timing: Mapped[str | None] = mapped_column(String(255), nullable=True)
    duration: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    prescription: Mapped["Prescription"] = relationship("Prescription", back_populates="medications", foreign_keys=[prescription_id])
    inventory: Mapped[Optional["Inventory"]] = relationship("Inventory", foreign_keys=[inventory_id])
    inventory_batch: Mapped[Optional["Batch"]] = relationship("Batch", foreign_keys=[inventory_batch_id])
