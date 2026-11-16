from fastapi import HTTPException
import re
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.Enum.SalesStatus import SalesStatus
from app.model.Branch import Branch
from app.model.Sale import Sale
from app.model.Product import Product
from app.model.Inventory import Batch


def generate_invoice_number(db: Session, branch_id: str) -> str:
    branch = db.query(Branch).filter(Branch.id == branch_id).first()

    clean_name = re.sub(r'[^A-Z0-9]', '', branch.branch_name.upper()) if branch and branch.branch_name else "BRANCH"
    branch_code = clean_name[:4] if len(clean_name) >= 4 else clean_name.ljust(4, 'X')
    year = datetime.now().year

    last_sale = (
        db.query(Sale)
        .filter(Sale.branch_id == branch_id)
        .filter(Sale.invoice_number.like(f"INV-{branch_code}-{year}-%"))
        .order_by(Sale.created_at.desc())
        .first()
    )

    next_number = 1
    if last_sale and last_sale.invoice_number:
        try:
            next_number = int(last_sale.invoice_number.split("-")[-1]) + 1
        except (ValueError, IndexError):
            next_number = 1

    return f"INV-{branch_code}-{year}-{next_number:05d}"


def compute_base_unit_quantity(product: Optional[Product], quantity: float, sale_unit: str = "unit") -> float:
    packs_per_outer = float(product.packs_per_outer or 1) if product else 1.0
    conversion = float(product.conversion_factor or 1) if product else 1.0

    if sale_unit == "outer":
        return float(quantity * packs_per_outer * conversion)
    elif sale_unit == "inner":
        return float(quantity * conversion)
    return float(quantity)


def deduct_inventory_stock(db: Session, sales_status: str, inventory_batch_id: Optional[str], computed_base_qty: float):
    is_dispensed = sales_status == SalesStatus.DISPENSED.value or sales_status == "dispensed"
    if is_dispensed and inventory_batch_id:
        batch = db.query(Batch).filter(Batch.id == inventory_batch_id).first()
        if batch:
            if batch.base_unit_qty < computed_base_qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock in batch {batch.batch_no}. Available: {batch.base_unit_qty}, Requested: {computed_base_qty}"
                )

            batch.base_unit_qty -= computed_base_qty

            if batch.inner_pack_qty and batch.base_unit_qty > 0:
                tablets_per_strip = batch.base_unit_qty / batch.inner_pack_qty
                if tablets_per_strip > 0:
                    batch.inner_pack_qty = max(0.0, batch.inner_pack_qty - (computed_base_qty / tablets_per_strip))

            if batch.quantity and batch.base_unit_qty > 0:
                tablets_per_box = batch.base_unit_qty / batch.quantity
                if tablets_per_box > 0:
                    batch.quantity = max(0.0, batch.quantity - (computed_base_qty / tablets_per_box))


def restore_inventory_stock(db: Session, inventory_batch_id: Optional[str], computed_base_qty: float):
    if inventory_batch_id and computed_base_qty > 0:
        batch = db.query(Batch).filter(Batch.id == inventory_batch_id).first()
        if batch:
            tablets_per_strip = (batch.base_unit_qty / batch.inner_pack_qty) if (batch.inner_pack_qty and batch.inner_pack_qty > 0) else 0
            tablets_per_box = (batch.base_unit_qty / batch.quantity) if (batch.quantity and batch.quantity > 0) else 0

            batch.base_unit_qty += computed_base_qty

            if tablets_per_strip > 0 and batch.inner_pack_qty:
                batch.inner_pack_qty += (computed_base_qty / tablets_per_strip)

            if tablets_per_box > 0 and batch.quantity:
                batch.quantity += (computed_base_qty / tablets_per_box)


