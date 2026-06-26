from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserRefreshTokenBase(BaseModel):
    user_id: str
    token: str
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None


class UserRefreshTokenCreate(UserRefreshTokenBase):
    pass


class UserRefreshTokenUpdate(BaseModel):
    token: Optional[str] = None
    expires_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None


class UserRefreshTokenResponse(UserRefreshTokenBase):
    id: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
