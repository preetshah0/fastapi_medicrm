from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.db.schemas.role import RoleResponse


class ProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    role: str
    status: str
    description: Optional[str] = None
    profile_photo: Optional[str] = None
    organization_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    roles: List[RoleResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    specialization: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=200)
    profile_photo: Optional[str] = Field(default=None, max_length=255)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)

    @model_validator(mode="after")
    def verify_password_match(self):
        if self.new_password != self.confirm_password:
            raise ValueError("New password and confirm password do not match")
        if self.current_password == self.new_password:
            raise ValueError("New password cannot be the same as the current password")
        return self


class OrganizationProfileResponse(BaseModel):
    id: str
    ref: str
    organization_name: str
    organization_email: str
    address: Optional[str] = None
    profile_photo: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OrganizationProfileUpdateRequest(BaseModel):
    organization_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    organization_email: Optional[str] = Field(default=None, max_length=255)
    address: Optional[str] = None
    profile_photo: Optional[str] = Field(default=None, max_length=255)

