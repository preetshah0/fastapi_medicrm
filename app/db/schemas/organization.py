from pydantic import BaseModel, ConfigDict, model_validator, Field
from datetime import time, datetime
from app.Enum.OrganizationStatus import OrganizationStatus
from typing import Optional
from app.db.schemas.user import UserResponse
from app.db.schemas.role import RoleResponse
from app.utils.validators import validate_operating_hours
from app.db.schemas.branch import BranchResponse

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
    owner_phone: str
    owner_specialization: str
    owner_description: str
    owner_profile_photo: str

    branch_name: str
    branch_address: str
    branch_phone: str
    branch_email: str
    opening_time: time = Field(json_schema_extra={"example": "09:00:00"})
    closing_time: time = Field(json_schema_extra={"example": "18:00:00"})
    city: str
    state: str

    @model_validator(mode="after")
    def safety_net(self) -> "OrganizationUpdate":
        if self.opening_time and self.closing_time:
            validate_operating_hours(self.opening_time, self.closing_time)
        return self


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

    branch_name: Optional[str] = None
    branch_address: Optional[str] = None
    branch_phone: Optional[str] = None
    branch_email: Optional[str] = None
    opening_time: Optional[time] = Field(default=None, json_schema_extra={"example": "09:00:00"})
    closing_time: Optional[time] = Field(default=None, json_schema_extra={"example": "18:00:00"})
    city: str
    state: str

    @model_validator(mode="after")
    def safety_net(self) -> "OrganizationUpdate":
        if self.opening_time or self.closing_time:
            validate_operating_hours(self.opening_time, self.closing_time)
        return self

class OrganizationResponse(OrganizationBase):
    id: str
    ref: str
    status: OrganizationStatus = OrganizationStatus.ACTIVE
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    owner: Optional[UserResponse] = None
    roles: list[RoleResponse] = []
    branches: list[BranchResponse] = []

    model_config = ConfigDict(from_attributes=True)
