from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.Enum.MasterOptionType import MasterOptionType


class MasterOptionBase(BaseModel):
    type: MasterOptionType
    name: str
    description: Optional[str] = None
    is_active: bool = True


class MasterOptionCreate(MasterOptionBase):
    pass


class MasterOptionUpdate(BaseModel):
    type: Optional[MasterOptionType] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class MasterOptionResponse(MasterOptionBase):
    id: str
    organization_id: str
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MasterOptionDropdownResponse(BaseModel):
    id: str
    name: str

   


class MasterOptionTypeResponse(BaseModel):
    value: str
    label: str

model_config = ConfigDict(from_attributes=True)