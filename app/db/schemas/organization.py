from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.Enum.OrganizationStatus import OrganizationStatus
from typing import Optional

class OrganizationBase(BaseModel):
    organization_name: str
    organization_email: EmailStr
    address: Optional[str] = None
    # annual_discount: Optional[float] = 0.0
    # plan_type: OrganizationPlanType = OrganizationPlanType.MONTHLY
    status: OrganizationStatus = OrganizationStatus.ACTIVE
    profile_photo: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    organization_name: Optional[str] = None
    organization_email: Optional[EmailStr] = None
    address: Optional[str] = None
    # annual_discount: Optional[float] = 0.0
    # plan_type: Optional[str] = "monthly"
    status: Optional[str] = "active"
    profile_photo: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
