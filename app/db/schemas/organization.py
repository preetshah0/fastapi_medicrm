from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.Enum.OrganizationStatus import OrganizationStatus
from typing import Optional
from app.db.schemas.user import UserResponse
from app.db.schemas.role import RoleResponse

class OrganizationBase(BaseModel):
    organization_name: str
    organization_email: str
    address: Optional[str] = None
    # annual_discount: Optional[float] = 0.0
    # plan_type: OrganizationPlanType = OrganizationPlanType.MONTHLY
    profile_photo: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    owner_name: str
    owner_email: str
    password: str
    owner_phone: Optional[str] = None
    owner_specialization: Optional[str] = None
    owner_description: Optional[str] = None
    owner_profile_photo: Optional[str] = None

class OrganizationUpdate(BaseModel):
    organization_name: Optional[str] = None
    organization_email: Optional[str] = None
    address: Optional[str] = None
    # annual_discount: Optional[float] = 0.0
    # plan_type: Optional[str] = "monthly"
    status: Optional[OrganizationStatus] = None
    profile_photo: Optional[str] = None

    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    owner_phone: Optional[str] = None
    owner_specialization: Optional[str] = None
    owner_description: Optional[str] = None
    owner_profile_photo: Optional[str] = None

class OrganizationResponse(OrganizationBase):
    id: str
    ref: str
    status: OrganizationStatus = OrganizationStatus.ACTIVE
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    owner: Optional[UserResponse] = None
    roles: list[RoleResponse] = []

    model_config = ConfigDict(from_attributes=True)
