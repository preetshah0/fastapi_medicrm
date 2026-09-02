from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from app.Enum.SalesStatus import SalesStatus
from app.Enum.SaleType import SaleType
from app.Enum.SalePaymentStatus import SalePaymentStatus
from app.Enum.SalePaymentMethod import SalePaymentMethod


class SaleItemBase(BaseModel):
    product_id: str
    inventory_id: Optional[str] = None
    inventory_batch_id: Optional[str] = None
    sale_unit: str
    quantity: float = Field(ge=0.0)
    base_unit_quantity: float = Field(ge=0.0)
    unit_price: float = Field(ge=0.0)
    discount: float = Field(ge=0.0)
    final_amount: float = Field(ge=0.0)


class SaleItemCreate(SaleItemBase):
    pass


class SaleItemUpdate(BaseModel):
    product_id: Optional[str] = None
    inventory_id: Optional[str] = None
    inventory_batch_id: Optional[str] = None
    sale_unit: Optional[str] = None
    quantity: Optional[float] = Field(default=None, ge=0.0)
    base_unit_quantity: Optional[float] = Field(default=None, ge=0.0)
    unit_price: Optional[float] = Field(default=None, ge=0.0)
    discount: Optional[float] = Field(default=None, ge=0.0)
    final_amount: Optional[float] = Field(default=None, ge=0.0)


class SaleItemResponse(SaleItemBase):
    id: str
    sale_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -------------------------------------------------------------------------------------------- #


class SaleBase(BaseModel):
    branch_id: str
    patient_id: Optional[str] = None
    prescription_id: Optional[str] = None
    name: str
    phone: Optional[str] = None
    notes: Optional[str] = None
    address: Optional[str] = None
    total_amount: float = Field(ge=0.0)
    discount_amount: float = Field(ge=0.0)
    sub_total: float = Field(ge=0.0)
    tax_amount: float = Field(ge=0.0)
    payment_status: Optional[SalePaymentStatus] = SalePaymentStatus.PENDING
    payment_method: Optional[SalePaymentMethod] = None
    sales_status: SalesStatus = SalesStatus.PENDING
    sales_type: SaleType


class SaleCreate(SaleBase):
    items: List[SaleItemCreate] = []


class SaleUpdate(BaseModel):
    branch_id: Optional[str] = None
    patient_id: Optional[str] = None
    prescription_id: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    address: Optional[str] = None
    total_amount: Optional[float] = Field(default=None, ge=0.0)
    discount_amount: Optional[float] = Field(default=None, ge=0.0)
    sub_total: Optional[float] = Field(default=None, ge=0.0)
    tax_amount: Optional[float] = Field(default=None, ge=0.0)
    payment_status: Optional[SalePaymentStatus] = None
    payment_method: Optional[SalePaymentMethod] = None
    sales_status: Optional[SalesStatus] = None
    sales_type: Optional[SaleType] = None


class DispenseSaleRequest(BaseModel):
    payment_method: SalePaymentMethod
    payment_status: Optional[SalePaymentStatus] = SalePaymentStatus.PAID
    notes: Optional[str] = None


class SaleResponse(SaleBase):
    id: str
    invoice_number: str
    organization_id: str
    created_at: datetime
    updated_at: datetime
    items: List[SaleItemResponse] = []

class SaleBranchResponse(BaseModel):
    id: str
    branch_name: str

class SaleEnumResponse(BaseModel):
    label: str
    value: str

    model_config = ConfigDict(from_attributes=True)


class SalePrescriptionResponse(BaseModel):
    id: str
    ref: str

    model_config = ConfigDict(from_attributes=True)
