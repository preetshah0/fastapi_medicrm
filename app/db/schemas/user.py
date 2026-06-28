from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from app.Enum.UserRole import UserRole
from app.Enum.UserStatus import UserStatus
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    specialization: Optional[str] = None
    role: UserRole = UserRole.STAFF
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
    status: Optional[bool] = None
    description: Optional[str] = None
    profile_photo: Optional[str] = None

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
