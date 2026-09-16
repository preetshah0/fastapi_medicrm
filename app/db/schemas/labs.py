from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional
from datetime import datetime, date, time

from app.Enum.LaboratoryFacilityType import LaboratoryFacilityType
from app.Enum.LaboratoryLabType import LaboratoryLabType
from app.Enum.LaboratoryStatus import LaboratoryStatus

class LabBase(BaseModel):
    name: str
    contact_person: str
    facility_type: LaboratoryFacilityType
    lab_type: Optional[str] = None
    lab_type_id: Optional[str] = None
    address: str
    city: str
    pincode: str
    phone_number: str
    email: str
    notes: str
    status: LaboratoryStatus

class LabCreate(LabBase):
    pass

class LabUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    facility_type: Optional[LaboratoryFacilityType] = None
    lab_type: Optional[str] = None
    lab_type_id: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[LaboratoryStatus] = None

class LabResponse(LabBase):
    id: str
    organization_id: str
    branch_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LabEnumResponse(BaseModel):
    value: str
    label: str

    model_config = ConfigDict(from_attributes=True)


class LabDropdownResponse(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)




class LabVisitBase(BaseModel):
    visited_date: Optional[date] = None
    visit_time: Optional[time] = None
    name: Optional[str] = None
    email: Optional[str] = None
    speciality: Optional[str] = None
    from_facility: Optional[str] = None
    notes: Optional[str] = None

class LabVisitCreate(LabVisitBase):
    lab_id: Optional[str] = None
    facility_type: LaboratoryFacilityType

    @model_validator(mode='after')
    def validate_fields_based_on_facility(self):
        from app.utils.validators import validate_lab_visit_fields
        return validate_lab_visit_fields(self.__class__, self)


class LabVisitResponse(LabVisitBase):
    id: str
    lab_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
