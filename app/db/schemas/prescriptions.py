from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date, time
from typing import Optional, List
from app.Enum.PrescriptionStatus import PrescriptionStatus
from app.Enum.FollowupDuration import FollowupDuration
from .followups import FollowUpResponse


class PrescriptionMedicationBase(BaseModel):
    inventory_id: str
    inventory_batch_id: str
    drug_name: str
    quantity: int = Field(default=1, ge=1)
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    meal_timing: Optional[str] = None
    duration: Optional[str] = None
    notes: Optional[str] = None


class PrescriptionMedicationCreate(PrescriptionMedicationBase):
    pass


class PrescriptionMedicationUpdate(BaseModel):
    inventory_id: Optional[str] = None
    inventory_batch_id: Optional[str] = None
    drug_name: Optional[str] = None
    quantity: Optional[int] = Field(default=None, ge=1)
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    meal_timing: Optional[str] = None
    duration: Optional[str] = None
    notes: Optional[str] = None


class PrescriptionMedicationResponse(PrescriptionMedicationBase):
    id: str
    prescription_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


#--------------------------------------------------------------------------------------------#

class PrescriptionBase(BaseModel):
    branch_id: str
    patient_id: str
    doctor_id: str
    ref: str
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    status: PrescriptionStatus = PrescriptionStatus.DRAFT
    follow_up_required: bool = False
    follow_up_date: Optional[date] = None
    follow_up_time: Optional[time] = None
    follow_up_note: Optional[str] = None
    followup_duration: Optional[FollowupDuration] = None


class PrescriptionCreate(PrescriptionBase):
    medications: List[PrescriptionMedicationCreate] = []


class PrescriptionUpdate(BaseModel):
    branch_id: Optional[str] = None
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None
    ref: Optional[str] = None
    diagnosis: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[PrescriptionStatus] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[date] = None
    follow_up_time: Optional[time] = None
    follow_up_note: Optional[str] = None
    followup_duration: Optional[FollowupDuration] = None



class PrescriptionResponse(PrescriptionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    medications: List[PrescriptionMedicationResponse] = []
    followup: Optional[FollowUpResponse] = None

    model_config = ConfigDict(from_attributes=True)


class MedicationDropdownResponse(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class FollowupDurationOptionResponse(BaseModel):
    value: int
    label: str

