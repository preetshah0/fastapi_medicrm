from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.Enum.UserStatus import UserStatus
from typing import Optional
from app.db.schemas.role import RoleResponse

class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    role: str = "staff"
    status: UserStatus = UserStatus.ACTIVE
    description: Optional[str] = None
    profile_photo: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    role: Optional[str] = None
    status: Optional[UserStatus] = None
    description: Optional[str] = None
    profile_photo: Optional[str] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    roles: list[RoleResponse] = []

    model_config = ConfigDict(from_attributes=True)


class DoctorDropdownResponse(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserDropdownResponse(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)

