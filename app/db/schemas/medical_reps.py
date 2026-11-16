from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.Enum.MRVisitPurpose import MRVisitPurpose


class MedicalRepsBase(BaseModel):
    company_name: str
    company_email: str 
    company_phone: str 
    notes: str
    profile_photo: str
    city: str

class MedicalRepsCreate(MedicalRepsBase):
    # organization_id: str
    pass
class MedicalRepsUpdate(MedicalRepsBase):
    company_name: Optional[str] = None
    company_email: Optional[str] = None
    company_phone: Optional[str] = None
    notes: Optional[str] = None
    profile_photo: Optional[str] = None
    city: Optional[str] = None

class MedicalRepsResponse(MedicalRepsBase):
    id: str
    organization_id: str
    branch_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



class MedicalRepVisitBase(BaseModel):
    reps_name: str
    visited_date: datetime
    notes: str
    visit_purpose: MRVisitPurpose
    Product: str

class MedicalRepVisitCreate(MedicalRepVisitBase):
    reps_id: str

class MedicalRepVisitUpdate(BaseModel):
    reps_name: Optional[str] = None
    visited_date: Optional[datetime] = None
    notes: Optional[str] = None
    visit_purpose: Optional[MRVisitPurpose] = None
    Product: Optional[str] = None

class MedicalRepVisitResponse(MedicalRepVisitBase):
    id: str
    reps_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
