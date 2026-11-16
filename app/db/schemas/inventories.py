from typing import List
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from app.Enum.InventoryStatus import InventoryStatus
from app.Enum.BatchStatus import BatchStatus




class InventoryBase(BaseModel):
    product_id: str
    inventory_status: InventoryStatus = InventoryStatus.IN_STOCK


class InventoryCreate(BaseModel):
    branch_id: str
    product_id: str


class InventoryUpdate(BaseModel):
    inventory_status: Optional[InventoryStatus] = None


class InventoryResponse(InventoryBase):
    id: str
    organization_id: str
    branch_id: str
    total_qty: int
    low_stock_threshold: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)



#-----------------------------------------------------------------------------------------------------------------------------------
class BatchBase(BaseModel):
    batch_no: str
    mfg_date: Optional[date] = None
    expiry_date: date
    initial_qty: int = Field(..., ge=0)
    current_quantity: int = Field(..., ge=0)
    subpack_qty: Optional[int] = Field(default=0, ge=0)
    base_unit_qty: Optional[int] = Field(default=0, ge=0)
    
    batch_cost_price: Decimal = Field(..., ge=0)
    mrp: Decimal = Field(..., ge=0)
    batch_selling_price: Decimal = Field(..., ge=0)
    base_unit_sp: Decimal = Field(..., ge=0)
    subpack_sp: Decimal = Field(..., ge=0)
    pack_sp: Decimal = Field(..., ge=0)

    is_active: bool = True
    batch_status: Optional[BatchStatus] = BatchStatus.IN_STOCK


class BatchCreate(BatchBase):
    inventory_id: Optional[str] = None
    product_id: Optional[str] = None
    supplier_id: str


class BatchUpdate(BaseModel):
    batch_no: Optional[str] = None
    mfg_date: Optional[date] = None
    expiry_date: Optional[date] = None
    initial_qty: Optional[int] = Field(default=None, ge=0)
    current_quantity: Optional[int] = Field(default=None, ge=0)
    subpack_qty: Optional[int] = Field(default=None, ge=0)
    base_unit_qty: Optional[int] = Field(default=None, ge=0)
    
    batch_cost_price: Optional[Decimal] = Field(default=None, ge=0)
    mrp: Optional[Decimal] = Field(default=None, ge=0)
    batch_selling_price: Optional[Decimal] = Field(default=None, ge=0)
    base_unit_sp: Optional[Decimal] = Field(default=None, ge=0)
    subpack_sp: Optional[Decimal] = Field(default=None, ge=0)
    pack_sp: Optional[Decimal] = Field(default=None, ge=0)

    supplier_id: Optional[str] = None
    is_active: Optional[bool] = None
    batch_status: Optional[BatchStatus] = None


class BatchResponse(BatchBase):
    id: str
    inventory_id: str
    product_id: str
    supplier_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BulkBatchCreateRequest(BaseModel):
    inventory_data: InventoryCreate
    batches: List[BatchCreate]
