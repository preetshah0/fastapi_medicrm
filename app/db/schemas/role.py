from pydantic import BaseModel, validator
from typing import List, Optional
from app.model.Roles import Permissions
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    slug: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    name: Optional[str] = None
    slug: Optional[str] = None


class RoleResponse(RoleBase):
    id: str
    slug: str
    permissions: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @validator("permissions", pre=True, each_item=True)
    def convert_permissions_to_strings(cls, perm):
        if isinstance(perm, Permissions):
            return perm.permission
        return perm


# Alias kept for backwards compatibility
Role = RoleResponse


class PermissionBase(BaseModel):
    permission: str
    slug: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    permission: Optional[str] = None
    slug: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: str
    slug: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True