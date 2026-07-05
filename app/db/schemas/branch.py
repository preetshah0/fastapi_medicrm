from pydantic import BaseModel, ConfigDict, model_validator, Field
from datetime import datetime, time, timedelta
from typing import Optional, Any
from app.Enum.BranchStatus import BranchStatus
from app.utils.validators import validate_operating_hours


class BaseBranch(BaseModel):
    branch_name: str
    branch_email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    status: BranchStatus = BranchStatus.ACTIVE
    city: str
    state: str


class BranchCreate(BaseBranch):
    opening_time: time = Field(json_schema_extra={"example": "09:00:00"})
    closing_time: time = Field(json_schema_extra={"example": "18:00:00"})
    
    @model_validator(mode="after")
    def safety_net(self) -> "BranchCreate":
        if self.opening_time and self.closing_time:
            validate_operating_hours(self.opening_time, self.closing_time)
        return self


class BranchUpdate(BaseModel):
    branch_name: Optional[str] = None
    branch_email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    status: Optional[BranchStatus] = None
    city: Optional[str] = None
    state: Optional[str] = None
    opening_time: Optional[time] = Field(default=None, json_schema_extra={"example": "09:00:00"})
    closing_time: Optional[time] = Field(default=None, json_schema_extra={"example": "18:00:00"})

    @model_validator(mode="after")
    def safety_net(self) -> "BranchUpdate":

        if self.opening_time or self.closing_time:
            validate_operating_hours(self.opening_time, self.closing_time)
        return self


class BranchResponse(BaseBranch):
    id: str
    organization_id: str
    opening_time: time
    closing_time: time
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BranchUserBase(BaseModel):
    branch_id: str
    user_id: str
    role_id: str
    user_roles: Optional[Any] = None
    status: Optional[str] = "active"


class BranchUserAssignEntry(BaseModel):
    user_id: str
    role_id: str


class BranchUserAssignRequest(BaseModel):
    branch_id: str
    users: list[BranchUserAssignEntry]
    status: Optional[str] = "active"


class BranchUserCreate(BranchUserBase):
    pass


class BranchUserUpdate(BaseModel):
    branch_id: Optional[str] = None
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    status: Optional[str] = None


class BranchUserResponse(BranchUserBase):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
