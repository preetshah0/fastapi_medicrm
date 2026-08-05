from pydantic import BaseModel, ConfigDict
from datetime import datetime, date, time
from typing import Optional, List
from app.Enum.AppointmentStatus import AppointmentStatus
from app.Enum.AppointmentType import AppointmentType
from app.Enum.AppointmentDuration import AppointmentDuration
from app.Enum.PatientVisitPaymentMode import PatientVisitPaymentMode
from app.Enum.PatientVisitPaymentStatus import PatientVisitPaymentStatus
from app.db.schemas.patient import PatientAppointmentResponse, PatientVisitCreate, PatientVisitResponse

           
class AppointmentBase(BaseModel):
    appointment_date: date
    start_time: time
    status: AppointmentStatus
    type: AppointmentType
    duration_minutes: AppointmentDuration
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    branch_id: str
    doctor_id: str
    patient_id: str


class AppointmentUpdate(BaseModel):
    # branch_id: Optional[str] = None
    # doctor_id: Optional[str] = None
    # patient_id: Optional[str] = None
    appointment_date: Optional[date] = None
    location: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[AppointmentStatus] = None
    type: Optional[AppointmentType] = None
    duration_minutes: Optional[AppointmentDuration] = None
    notes: Optional[str] = None


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus
    payment_details: Optional[PatientVisitCreate] = None


class AppointmentSlotResponse(BaseModel):
    value: str
    label: str
    disabled: bool


class AppointmentDurationOptionResponse(BaseModel):
    value: int
    label: str


class AppointmentResponse(AppointmentBase):
    id: str
    branch_id: str
    doctor_id: str
    patient_id: str
    location: str
    end_time: time
    created_at: datetime
    updated_at: datetime

    patient_appointments: List[PatientAppointmentResponse] = []
    patient_visits: List[PatientVisitResponse] = []

    model_config = ConfigDict(from_attributes=True)
