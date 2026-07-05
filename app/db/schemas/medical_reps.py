from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.Enum.MRVisitPurpose import MRVisitPurpose


class MedicalRepsBase(BaseModel):
    reps_name:str
    reps_email:str 
    reps_phone:str 
    notes: str
    reps_profile_photo: str
    company_name: str
    city: str

class MedicalRepsCreate(MedicalRepsBase):
    # organization_id: str
    pass
class MedicalRepsUpdate(MedicalRepsBase):
    reps_name: Optional[str] = None
    reps_email: Optional[str] = None
    reps_phone: Optional[str] = None
    notes: Optional[str] = None
    reps_profile_photo: Optional[str] = None
    company_name: Optional[str] = None
    city: Optional[str] = None

class MedicalRepsResponse(MedicalRepsBase):
    id: str
    organization_id: str
    branch_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class MedicalRepVisitBase(BaseModel):
    visited_date: datetime
    notes: str
    visit_purpose: MRVisitPurpose
    product: str

class MedicalRepVisitCreate(MedicalRepVisitBase):
    reps_id: str

class MedicalRepVisitUpdate(BaseModel):
    visited_date: Optional[datetime] = None
    notes: Optional[str] = None
    visit_purpose: Optional[MRVisitPurpose] = None
    product: Optional[str] = None

class MedicalRepVisitResponse(MedicalRepVisitBase):
    id: str
    reps_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
