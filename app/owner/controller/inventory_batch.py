from app.services.inventory_service import inventory_count
from app.db.schemas import BatchUpdate
from app.db.schemas import InventoryUpdate
from app.services.inventory_service import calculate_inventory_status
from app.model.Supplier import Supplier
from datetime import date
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.model.Product import Product
from app.model.Inventory import Inventory, Batch
from app.db.schemas import InventoryCreate, BatchCreate
from app.Enum.InventoryStatus import InventoryStatus
from app.Enum.BatchStatus import BatchStatus
from app.services.inventory_service import (
    calculate_batch_status,
    calculate_inventory_status,
    sync_inventory_status,
)
from app.db.schemas.master_options import MasterOptionDropdownResponse
from app.db.schemas.suppliers import SupplierDropdownResponse

from app.services.product_service import (
    calculate_unit_quantities,
    calculate_tier_selling_prices,
)


def format_medicine_name(product: Product) -> str:
    parts = [product.name]
    if product.variant:
        parts.append(f"({product.variant})")
    if product.dosage_strength:
        parts.append(f"({product.dosage_strength})")
    return " ".join(parts)


def get_medicine_dropdown(
    db: Session,
    organization_id: str,
    branch_id: str
):
    products = (
        db.query(Product.id, Product.name, Product.variant, Product.dosage_strength)
        .filter(
            Product.organization_id == organization_id,
            Product.branch_id == branch_id,
            Product.is_available == True
        )
        .all()
    )
    
    medicine_dropdown =  [
        MasterOptionDropdownResponse(
            id=product.id,
            name=format_medicine_name(product)
        )
        for product in products
    ]
    return medicine_dropdown


def get_supplier_dropdown(
    db: Session, 
    organization_id: str, 
    branch_id: str
):

    results = db.query(Supplier.id, Supplier.company).filter(
        Supplier.organization_id == organization_id,
        Supplier.branch_id == branch_id,
    ).all()

    return [
        SupplierDropdownResponse(
            id=row.id,
            company=row.company or "Unnamed Supplier"
        )
        for row in results
    ]



def get_or_create_inventory(
    db: Session,
    inventory_data: InventoryCreate,
    organization_id: str
):
    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.organization_id == organization_id,
            Inventory.branch_id == inventory_data.branch_id,
            Inventory.product_id == inventory_data.product_id
        )
        .first()
    )

    if not inventory:
        product = (
            db.query(Product)
            .filter(
                Product.id == inventory_data.product_id,
                Product.organization_id == organization_id
            )
            .first()
        )
        inventory = Inventory(
            organization_id=organization_id,
            branch_id=inventory_data.branch_id,
            product_id=inventory_data.product_id,
            low_stock_threshold=product.low_stock_threshold if product else 1,
            total_qty=0,
            inventory_status=InventoryStatus.OUT_OF_STOCK.value,
        )
        db.add(inventory)
        db.commit()
        db.refresh(inventory)

    return inventory


def create_inventory_batch(
    db: Session,
    batch_data: BatchCreate,
    inventory_data: InventoryCreate,
    organization_id: str
):
    product = (
        db.query(Product)
        .filter(
            Product.id == inventory_data.product_id,
            Product.organization_id == organization_id,
            Product.branch_id == inventory_data.branch_id
        )
        .first()
    )

    # Use product_service to compute unit quantities if not provided
    calculated_qty = calculate_unit_quantities(
        initial_outer_qty=batch_data.initial_qty,
        packs_per_outer=product.packs_per_outer if product else 1,
        conversion_factor=product.conversion_factor if product else 1
    )
    
    subpack_qty = batch_data.subpack_qty or calculated_qty.subpack_qty
    base_unit_qty = batch_data.base_unit_qty or calculated_qty.base_unit_qty

    # Use product_service to compute tier prices if not provided
    calculated_prices = calculate_tier_selling_prices(
        base_unit_sp=batch_data.base_unit_sp,
        conversion_factor=product.conversion_factor if product else 1,
        packs_per_outer=product.packs_per_outer if product else 1
    )

    subpack_sp = batch_data.subpack_sp or calculated_prices.subpack_sp
    pack_sp = batch_data.pack_sp or calculated_prices.pack_sp

    batch_status = calculate_batch_status(
        expiry_date=batch_data.expiry_date,
        current_quantity=batch_data.initial_qty
    )

    # 1. Get or create Inventory record
    inventory = get_or_create_inventory(
        db=db,
        inventory_data=inventory_data,
        organization_id=organization_id
    )

    # 2. Create Batch record
    new_batch = Batch(
        inventory_id=inventory.id,
        product_id=inventory_data.product_id,
        supplier_id=batch_data.supplier_id,
        batch_no=batch_data.batch_no,
        mfg_date=batch_data.mfg_date,
        expiry_date=batch_data.expiry_date,
        initial_qty=batch_data.initial_qty,
        current_quantity=batch_data.initial_qty,
        subpack_qty=subpack_qty,
        base_unit_qty=base_unit_qty,
        batch_cost_price=batch_data.batch_cost_price,
        mrp=batch_data.mrp,
        batch_selling_price=batch_data.batch_selling_price,
        base_unit_sp=batch_data.base_unit_sp,
        subpack_sp=subpack_sp,
        pack_sp=pack_sp,
        is_active=batch_data.is_active,
        batch_status=batch_status
    )
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    sync_inventory_status(db, inventory)

    return inventory, new_batch


def create_bulk_inventory_batches(
    db: Session,
    inventory_data: InventoryCreate,
    batches_data: List[BatchCreate],
    organization_id: str
):
    product = (
        db.query(Product)
        .filter(
            Product.id == inventory_data.product_id,
            Product.organization_id == organization_id,
            Product.branch_id == inventory_data.branch_id
        )
        .first()
    )

    # 1. Get or create Inventory record
    inventory = get_or_create_inventory(
        db=db,
        inventory_data=inventory_data,
        organization_id=organization_id
    )

    created_batches = []
    for batch_data in batches_data:
        # Use product_service to compute unit quantities if not provided
        calculated_qty = calculate_unit_quantities(
            initial_outer_qty=batch_data.initial_qty,
            packs_per_outer=product.packs_per_outer if product else 1,
            conversion_factor=product.conversion_factor if product else 1
        )
        
        subpack_qty = batch_data.subpack_qty or calculated_qty.subpack_qty
        base_unit_qty = batch_data.base_unit_qty or calculated_qty.base_unit_qty

        # Use product_service to compute tier prices if not provided
        calculated_prices = calculate_tier_selling_prices(
            base_unit_sp=batch_data.base_unit_sp,
            conversion_factor=product.conversion_factor if product else 1,
            packs_per_outer=product.packs_per_outer if product else 1
        )

        subpack_sp = batch_data.subpack_sp or calculated_prices.subpack_sp
        pack_sp = batch_data.pack_sp or calculated_prices.pack_sp

        batch_status = calculate_batch_status(
            expiry_date=batch_data.expiry_date,
            current_quantity=batch_data.initial_qty
        )

        new_batch = Batch(
            inventory_id=inventory.id,
            product_id=inventory_data.product_id,
            supplier_id=batch_data.supplier_id,
            batch_no=batch_data.batch_no,
            mfg_date=batch_data.mfg_date,
            expiry_date=batch_data.expiry_date,
            initial_qty=batch_data.initial_qty,
            current_quantity=batch_data.initial_qty,
            subpack_qty=subpack_qty,
            base_unit_qty=base_unit_qty,
            batch_cost_price=batch_data.batch_cost_price,
            mrp=batch_data.mrp,
            batch_selling_price=batch_data.batch_selling_price,
            base_unit_sp=batch_data.base_unit_sp,
            subpack_sp=subpack_sp,
            pack_sp=pack_sp,
            is_active=batch_data.is_active,
            batch_status=batch_status
        )
        db.add(new_batch)
        created_batches.append(new_batch)

    db.commit()
    for batch in created_batches:
        db.refresh(batch)

    # Sync total_qty and inventory_status once after adding all batches
    sync_inventory_status(db, inventory)

    return inventory, created_batches




def update_inventory(
    db: Session,
    inventory_id: str,
    inventory_data: InventoryUpdate,
    organization_id: str
):
    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.id == inventory_id,
            Inventory.organization_id == organization_id
        )
        .first()
    )

    update_dict = inventory_data.model_dump(exclude_unset=True)
    if "inventory_status" in update_dict and update_dict["inventory_status"] is not None:
        update_dict["inventory_status"] = update_dict["inventory_status"].value

    for key, value in update_dict.items():
        setattr(inventory, key, value)

    db.commit()
    db.refresh(inventory)
    return inventory


def delete_inventory(
    db: Session,
    inventory_id: str,
    organization_id: str
) -> bool:
    inventory = (
        db.query(Inventory)
        .filter(
            Inventory.id == inventory_id,
            Inventory.organization_id == organization_id
        )
        .first()
    )
    if not inventory:
        return False

    db.delete(inventory)
    db.commit()
    return True



def update_batch(
    db: Session,
    batch_id: str,
    batch_data: BatchUpdate,
    organization_id: str
):
    batch = (
        db.query(Batch)
        .join(Inventory, Batch.inventory_id == Inventory.id)
        .filter(
            Batch.id == batch_id,
            Inventory.organization_id == organization_id
        )
        .first()
    )

    update_dict = batch_data.model_dump(exclude_unset=True)

    if "batch_status" in update_dict and update_dict["batch_status"] is not None:
        update_dict["batch_status"] = update_dict["batch_status"].value

    for key, value in update_dict.items():
        setattr(batch, key, value)

    batch.batch_status = calculate_batch_status(
        expiry_date=batch.expiry_date,
        current_quantity=batch.current_quantity
    )

    db.commit()
    db.refresh(batch)

  
    inventory = db.query(Inventory).filter(Inventory.id == batch.inventory_id).first()
    if inventory:
        sync_inventory_status(db, inventory)

    return batch


def delete_batch(
    db: Session,
    batch_id: str,
    organization_id: str
):
    batch = (
        db.query(Batch)
        .join(Inventory, Batch.inventory_id == Inventory.id)
        .filter(
            Batch.id == batch_id,
            Inventory.organization_id == organization_id
        )
        .first()
    )
    
    inventory_id = batch.inventory_id
    db.delete(batch)
    db.commit()
    
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if inventory:
        sync_inventory_status(db, inventory)

    return True



def get_inventories(
    db: Session,
    organization_id: str,
    branch_id: Optional[str] = None,
    inventory_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Inventory).filter(Inventory.organization_id == organization_id)
    if branch_id:
        query = query.filter(Inventory.branch_id == branch_id)
    if inventory_status:
        query = query.filter(Inventory.inventory_status == inventory_status)
    return query.offset(skip).limit(limit).all()


def get_inventory_by_id(
    db: Session,
    inventory_id: str,
    organization_id: str
):
    return (
        db.query(Inventory)
        .filter(
            Inventory.id == inventory_id,
            Inventory.organization_id == organization_id
        )
        .first()
    )


def get_batches_by_inventory_id(
    db: Session,
    inventory_id: str,
    organization_id: str,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Batch)
        .join(Inventory, Batch.inventory_id == Inventory.id)
        .filter(
            Batch.inventory_id == inventory_id,
            Inventory.organization_id == organization_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_batch_by_id(
    db: Session,
    batch_id: str,
    organization_id: str
):
    return (
        db.query(Batch)
        .join(Inventory, Batch.inventory_id == Inventory.id)
        .filter(
            Batch.id == batch_id,
            Inventory.organization_id == organization_id
        )
        .first()
    )