from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime, date
from app.Enum.SupplierVisitPurpose import SupplierVisitPurpose
from app.Enum.SupplierType import SupplierType

class SupplierBase(BaseModel):
    type: SupplierType
    company: Optional[str] = None
    email: str
    phone: str
    notes: str

class SupplierCreate(SupplierBase):
    reps_id: Optional[str] = None

class SupplierUpdate(BaseModel):
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    reps_id: Optional[str] = None

class SupplierResponse(SupplierBase):
    id: str
    organization_id: str
    branch_id: str
    reps_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SupplierVisitBase(BaseModel):
    supplier_name: str
    visited_date: date = Field(default=None, json_schema_extra={"example": "2026-07-05"})
    visit_purpose: SupplierVisitPurpose
    notes: str

class SupplierVisitCreate(SupplierVisitBase):
    pass
# class SupplierVisitUpdate(BaseModel):
#     supplier_name: Optional[str] = None
#     visited_date: Optional[datetime] = None
#     batch_number: Optional[str] = None
#     visit_purpose: Optional[SupplierVisitPurpose] = None
#     notes: Optional[str] = None

class SupplierVisitResponse(SupplierVisitBase):
    id: str
    supplier_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
