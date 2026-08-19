from pydantic import BaseModel, ConfigDict
from datetime import datetime, date, time
from typing import Optional
from app.Enum.FollowupStatus import FollowupStatus
from app.Enum.FollowupVisitStatus import FollowupVisitStatus


class FollowUpResponse(BaseModel):
    id: str
    organization_id: str
    branch_id: str
    patient_id: str
    doctor_id: str
    appointment_id: Optional[str] = None
    prescription_id: Optional[str] = None
    followable_type: str
    followable_id: str
    followup_date: Optional[date] = None
    followup_time: Optional[time] = None
    followup_duration: int = 30
    status: FollowupStatus = FollowupStatus.SCHEDULED
    visited_status: FollowupVisitStatus = FollowupVisitStatus.PENDING
    contacted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RescheduleFollowupRequest(BaseModel):
    new_date: date
    new_time: Optional[time] = None
    new_duration: Optional[int] = None

