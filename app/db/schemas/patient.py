from pydantic import BaseModel, ConfigDict
from datetime import datetime, date, time
from typing import Optional, List
from app.Enum.PatientGender import PatientGender
from app.Enum.PatientBloodGroup import PatientBloodGroup
from app.Enum.PatientVisitPaymentMode import PatientVisitPaymentMode
from app.Enum.PatientVisitPaymentStatus import PatientVisitPaymentStatus
from app.Enum.AppointmentDuration import AppointmentDuration


# -----------------
# Note Schemas
# -----------------
class NoteBase(BaseModel):
    notes: str
    note_date: Optional[date] = None


class NoteCreate(NoteBase):
    patient_id: str


class NoteUpdate(BaseModel):
    notes: Optional[str] = None
    note_date: Optional[date] = None


class NoteResponse(NoteBase):
    id: str
    patient_id: str
    user_id: str
    written_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Report Schemas
# -----------------
class ReportBase(BaseModel):
    report_type: str
    attachment: Optional[str] = None
    notes: Optional[str] = None
    report_date: Optional[date] = None


class ReportCreate(ReportBase):
    patient_id: str


class ReportUpdate(BaseModel):
    report_type: Optional[str] = None
    attachment: Optional[str] = None
    notes: Optional[str] = None
    report_date: Optional[date] = None


class ReportResponse(ReportBase):
    id: str
    patient_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Patient Appointment Log (System Managed Read Schema)
# -----------------
class PatientAppointmentResponse(BaseModel):
    id: str
    appointment_id: str
    patient_id: str
    location: str
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    duration_minutes: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Patient Visit Log (System Managed Read Schema)
# -----------------
class PatientVisitCreate(BaseModel):
    amount_charged: float
    payment_mode: PatientVisitPaymentMode
    payment_status: PatientVisitPaymentStatus

class PatientVisitResponse(BaseModel):
    id: str
    appointment_id: str
    patient_id: str
    visited_date: date
    visit_time: time
    amount_charged: float
    payment_mode: PatientVisitPaymentMode
    payment_status: PatientVisitPaymentStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Patient Schemas
# -----------------
class PatientBase(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    gender: PatientGender
    address: Optional[str] = None
    blood_group: PatientBloodGroup
    description: str
    profile_photo: Optional[str] = None


class PatientCreate(PatientBase):
    organization_id: str


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[PatientGender] = None
    address: Optional[str] = None
    blood_group: Optional[PatientBloodGroup] = None
    description: Optional[str] = None
    profile_photo: Optional[str] = None


class PatientResponse(PatientBase):
    id: str
    user_id: Optional[str] = None
    organization_id: str
    ref_code: str
    created_at: datetime
    updated_at: datetime

    notes: List[NoteResponse] = []
    reports: List[ReportResponse] = []
    patient_appointments: List[PatientAppointmentResponse] = []
    patient_visits: List[PatientVisitResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PatientDropdownResponse(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)

