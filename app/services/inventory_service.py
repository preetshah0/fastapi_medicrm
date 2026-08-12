from datetime import date
from sqlalchemy.orm import Session
from app.model.Product import Product
from app.model.Inventory import Inventory, Batch
from app.db.schemas import BatchCreate
from app.Enum.InventoryStatus import InventoryStatus
from app.Enum.BatchStatus import BatchStatus


def calculate_batch_status(expiry_date: date, current_quantity: int) -> str:
    today = date.today()
    if expiry_date and expiry_date < today:
        status =  BatchStatus.EXPIRED.value
    elif current_quantity == 0 and expiry_date > today:
        status = BatchStatus.COMPLETED.value
    else:
        status = BatchStatus.IN_STOCK.value
        
    return status

def calculate_inventory_status(total_quantity: int, low_stock_threshold: int) -> str:
    if total_quantity == 0:
        inven_status =  InventoryStatus.OUT_OF_STOCK.value
    elif total_quantity <= low_stock_threshold:
        inven_status = InventoryStatus.LOW_STOCK.value
    else:
        inven_status = InventoryStatus.IN_STOCK.value

    return inven_status


def calculate_subpack_qty(initial_qty: int, base_unit_qty: int, conversion_factor: int):
    return initial_qty * conversion_factor - base_unit_qty



def inventory_count(db: Session, inventory: Inventory) -> int:
    all_batches = db.query(Batch).filter(Batch.inventory_id == inventory.id).all()
    total_quantity = sum(b.current_quantity for b in all_batches if b.is_active)
    return total_quantity


def sync_inventory_status(db: Session, inventory: Inventory) -> Inventory:
    product = db.query(Product).filter(Product.id == inventory.product_id).first()
    total_quantity = inventory_count(db, inventory)

    inventory.total_qty = total_quantity
    inventory.inventory_status = calculate_inventory_status(
        total_quantity=total_quantity,
        low_stock_threshold=product.low_stock_threshold if product else 1
    )
    db.commit()
    db.refresh(inventory)
    return inventory
   

