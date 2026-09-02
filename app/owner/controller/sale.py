import re
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.schemas import SaleCreate, SaleUpdate
from app.Enum.BatchStatus import BatchStatus
from app.Enum.SalePaymentMethod import SalePaymentMethod
from app.Enum.SalePaymentStatus import SalePaymentStatus
from app.Enum.SalesStatus import SalesStatus
from app.Enum.SaleType import SaleType
from app.Enum.PrescriptionStatus import PrescriptionStatus
from app.db.schemas.sales import SaleBranchResponse, SaleEnumResponse, SalePrescriptionResponse
from app.model.Branch import Branch
from app.model.Sale import Sale, SaleItem
from app.model.Prescription import Prescription
from app.model.Patient import Patient
from app.model.Product import Product
from app.model.Inventory import Batch
from app.services.sale_service import (
    generate_invoice_number,
    compute_base_unit_quantity,
    deduct_inventory_stock,
    restore_inventory_stock,
)



def get_branch(db: Session, organization_id: Optional[str] = None):
    query = db.query(Branch.id, Branch.branch_name).filter(Branch.status == BatchStatus.ACTIVE)
    if organization_id:
        query = query.filter(Branch.organization_id == organization_id)
    db_branch = query.all()
    return [SaleBranchResponse(id=row.id, branch_name=row.branch_name) for row in db_branch]


def get_prescription(db: Session, organization_id: Optional[str] = None):
    query = db.query(Prescription.id, Prescription.ref).filter(
        Prescription.status == PrescriptionStatus.FINALIZED.value
    )
    if organization_id:
        query = query.join(Branch, Prescription.branch_id == Branch.id).filter(
            Branch.organization_id == organization_id
        )
    db_prescription = query.all()
    return [SalePrescriptionResponse(id=row.id, ref=row.ref) for row in db_prescription]


def get_sale_types():
    return [
        SaleEnumResponse(
            value=types.value,
            label=types.label
        )
        for types in SaleType
    ]


def get_sale_payment_method_types():
    return [
        SaleEnumResponse(
            value=types.value,
            label=types.label
        )
        for types in SalePaymentMethod
    ]


def get_sale_payment_status_types():
    return [
        SaleEnumResponse(
            value=types.value,
            label=types.label
        )
        for types in SalePaymentStatus
    ]


def get_sales_status_types():
    return [
        SaleEnumResponse(
            value=types.value,
            label=types.label
        )
        for types in SalesStatus
    ]


def create_sale(db: Session, sale_data: SaleCreate) -> Sale:
    branch = db.query(Branch).filter(Branch.id == sale_data.branch_id).first()

    patient = db.query(Patient).filter(Patient.id == sale_data.patient_id).first() if sale_data.sales_type.value == SaleType.INTERNAL.value and sale_data.patient_id else None

    db_sale = Sale(
        organization_id=branch.organization_id if branch else None,
        branch_id=sale_data.branch_id,
        patient_id=sale_data.patient_id,
        prescription_id=sale_data.prescription_id,
        invoice_number=generate_invoice_number(db, sale_data.branch_id),
        name=patient.name if patient else (sale_data.name or "Walk-in Customer"),
        phone=patient.phone if patient else sale_data.phone,
        notes=sale_data.notes,
        address=sale_data.address,
        total_amount=sale_data.total_amount,
        discount_amount=sale_data.discount_amount,
        sub_total=sale_data.sub_total,
        tax_amount=sale_data.tax_amount,
        payment_status=sale_data.payment_status.value if sale_data.payment_status else SalePaymentStatus.UNPAID.value,
        payment_method=sale_data.payment_method.value if sale_data.payment_method else None,
        sales_status=sale_data.sales_status.value if sale_data.sales_status else SalesStatus.DRAFT.value,
        sales_type=sale_data.sales_type.value,
    )
    db.add(db_sale)
    db.flush()

    for item in sale_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        computed_base_qty = item.base_unit_quantity or compute_base_unit_quantity(
            product=product,
            quantity=item.quantity,
            sale_unit=item.sale_unit
        )

        db_item = SaleItem(
            sale_id=db_sale.id,
            product_id=item.product_id,
            inventory_id=item.inventory_id,
            inventory_batch_id=item.inventory_batch_id,
            sale_unit=item.sale_unit or "unit",
            quantity=item.quantity,
            base_unit_quantity=computed_base_qty,
            unit_price=item.unit_price,
            discount=item.discount,
            final_amount=item.final_amount,
        )
        db.add(db_item)

        deduct_inventory_stock(
            db=db,
            sales_status=db_sale.sales_status,
            inventory_batch_id=item.inventory_batch_id,
            computed_base_qty=computed_base_qty
        )

    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_sales(
    db: Session,
    organization_id: Optional[str] = None,
    branch_id: Optional[str] = None,
    patient_id: Optional[str] = None,
    sales_status: Optional[str] = None,
    payment_status: Optional[str] = None,
    sales_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Sale]:
    query = db.query(Sale)
    if organization_id:
        query = query.filter(Sale.organization_id == organization_id)
    if branch_id:
        query = query.filter(Sale.branch_id == branch_id)
    if patient_id:
        query = query.filter(Sale.patient_id == patient_id)
    if sales_status:
        query = query.filter(Sale.sales_status == sales_status)
    if payment_status:
        query = query.filter(Sale.payment_status == payment_status)
    if sales_type:
        query = query.filter(Sale.sales_type == sales_type)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Sale.invoice_number.ilike(search_term)) |
            (Sale.name.ilike(search_term)) |
            (Sale.phone.ilike(search_term))
        )
    return query.order_by(Sale.created_at.desc()).offset(skip).limit(limit).all()


def get_sale_by_id(db: Session, sale_id: str, organization_id: Optional[str] = None) -> Sale:
    query = db.query(Sale).filter(Sale.id == sale_id)
    if organization_id:
        query = query.filter(Sale.organization_id == organization_id)
    sale = query.first()
    return sale


def update_sale(db: Session, sale_id: str, sale_data: SaleUpdate, organization_id: Optional[str] = None) -> Sale:
    sale = get_sale_by_id(db, sale_id, organization_id)
    old_status = sale.sales_status

    update_dict = sale_data.model_dump(exclude_unset=True)

    for field in ["payment_status", "payment_method", "sales_status", "sales_type"]:
        if field in update_dict and update_dict[field] is not None:
            val = update_dict[field]
            update_dict[field] = val.value if hasattr(val, "value") else str(val)

    for key, value in update_dict.items():
        setattr(sale, key, value)

    new_status = sale.sales_status

    if old_status != SalesStatus.DISPENSED.value and new_status == SalesStatus.DISPENSED.value:
        for item in sale.items:
            deduct_inventory_stock(
                db=db,
                sales_status=new_status,
                inventory_batch_id=item.inventory_batch_id,
                computed_base_qty=item.base_unit_quantity
            )
    elif old_status == SalesStatus.DISPENSED.value and new_status in [SalesStatus.CANCELLED.value, "cancelled"]:
        for item in sale.items:
            restore_inventory_stock(
                db=db,
                inventory_batch_id=item.inventory_batch_id,
                computed_base_qty=item.base_unit_quantity
            )

    db.commit()
    db.refresh(sale)
    return sale


def delete_sale(db: Session, sale_id: str, organization_id: Optional[str] = None) -> dict:
    sale = get_sale_by_id(db, sale_id, organization_id)

    if sale.sales_status == SalesStatus.DISPENSED.value:
        for item in sale.items:
            restore_inventory_stock(
                db=db,
                inventory_batch_id=item.inventory_batch_id,
                computed_base_qty=item.base_unit_quantity
            )

    db.delete(sale)
    db.commit()
    return True


def dispense_sale(
    db: Session,
    sale_id: str,
    payment_method: SalePaymentMethod,
    notes: Optional[str] = None,
    organization_id: Optional[str] = None,
) -> Sale:
    sale = get_sale_by_id(db, sale_id, organization_id)


    if sale.items:
        sale.sub_total = sum(item.final_amount for item in sale.items)
        sale.total_amount = max(0.0, (sale.sub_total - (sale.discount_amount or 0.0)) + (sale.tax_amount or 0.0))

    sale.payment_method = payment_method.value
    sale.payment_status = SalePaymentStatus.PAID.value
    sale.sales_status = SalesStatus.DISPENSED.value

    if notes:
        sale.notes = f"{sale.notes}\n{notes}" if sale.notes else notes

    for item in sale.items:
        deduct_inventory_stock(
            db=db,
            sales_status=SalesStatus.DISPENSED.value,
            inventory_batch_id=item.inventory_batch_id,
            computed_base_qty=item.base_unit_quantity,
        )

    db.commit()
    db.refresh(sale)
    return sale


def cancel_sale(
    db: Session,
    sale_id: str,
    organization_id: Optional[str] = None,
    notes: Optional[str] = None,
) -> Sale:
    sale = get_sale_by_id(db, sale_id, organization_id)

    sale.sales_status = SalesStatus.CANCELLED.value
    sale.payment_status = SalePaymentStatus.CANCELLED.value
    sale.payment_method = SalePaymentMethod.OTHER.value
    if notes:
        sale.notes = f"{sale.notes}\n[CANCELLED]: {notes}" if sale.notes else f"[CANCELLED]: {notes}"

    db.commit()
    db.refresh(sale)
    return sale