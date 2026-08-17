from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.inventories import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse,
    BatchCreate,
    BatchUpdate,
    BatchResponse,
    BulkBatchCreateRequest,
)
from app.db.schemas.master_options import MasterOptionDropdownResponse
from app.db.schemas.suppliers import SupplierDropdownResponse

from app.owner.controller.inventory_batch import (
    create_inventory_batch,
    create_bulk_inventory_batches,
    get_or_create_inventory,
    get_inventories,
    get_inventory_by_id,
    update_inventory,
    delete_inventory,
    get_batches_by_inventory_id,
    get_batch_by_id,
    update_batch,
    delete_batch,
    get_medicine_dropdown,
    get_supplier_dropdown,
)
from app.utils.ApiResponse import success_response, error_response, not_found_response

router = APIRouter(prefix="/owner/inventory", tags=["inventory"])


@router.post("/create/{organization_id}", response_model=APIResponse[InventoryResponse])
def create_inventory_route(
    organization_id: str,
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db)
):
    inventory = get_or_create_inventory(
        db=db,
        inventory_data=inventory_data,
        organization_id=organization_id
    )
    return success_response("Inventory created or retrieved successfully", inventory)


@router.post("/batch/create/{organization_id}", response_model=APIResponse[BatchResponse])
def create_inventory_batch_route(
    organization_id: str,
    inventory_data: InventoryCreate,
    batch_data: BatchCreate,
    db: Session = Depends(get_db)
):
    inventory, batch = create_inventory_batch(
        db=db,
        batch_data=batch_data,
        inventory_data=inventory_data,
        organization_id=organization_id
    )
    return success_response("Inventory batch created successfully", batch)


@router.post("/batch/create-bulk/{organization_id}", response_model=APIResponse[List[BatchResponse]])
def create_bulk_inventory_batches_route(
    organization_id: str,
    payload: BulkBatchCreateRequest,
    db: Session = Depends(get_db)
):
    inventory, batches = create_bulk_inventory_batches(
        db=db,
        inventory_data=payload.inventory_data,
        batches_data=payload.batches,
        organization_id=organization_id
    )
    return success_response("Bulk inventory batches created successfully", batches)


@router.get("/organization/{organization_id}", response_model=APIResponse[List[InventoryResponse]])
def get_all_inventories_route(
    organization_id: str,
    branch_id: Optional[str] = None,
    inventory_status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    inventories = get_inventories(
        db=db,
        organization_id=organization_id,
        branch_id=branch_id,
        inventory_status=inventory_status,
        skip=skip,
        limit=limit
    )
    return success_response("Inventories fetched successfully", inventories)


@router.get("/{inventory_id}/organization/{organization_id}", response_model=APIResponse[InventoryResponse])
def get_inventory_route(
    inventory_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    inventory = get_inventory_by_id(db=db, inventory_id=inventory_id, organization_id=organization_id)
    if not inventory:
        return not_found_response("Inventory record not found", data="")
    return success_response("Inventory fetched successfully", inventory)


@router.put("/{inventory_id}/organization/{organization_id}", response_model=APIResponse[InventoryResponse])
def update_inventory_route(
    inventory_id: str,
    organization_id: str,
    payload: InventoryUpdate,
    db: Session = Depends(get_db)
):
    result = update_inventory(
        db=db,
        inventory_id=inventory_id,
        inventory_data=payload,
        organization_id=organization_id
    )
    if not result:
        return not_found_response("Inventory record not found", data="")
    return success_response("Inventory updated successfully", result)


@router.delete("/{inventory_id}/organization/{organization_id}", response_model=APIResponse[str])
def delete_inventory_route(
    inventory_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    success = delete_inventory(db=db, inventory_id=inventory_id, organization_id=organization_id)
    if not success:
        return not_found_response("Inventory record not found", data="")
    return success_response("Inventory deleted successfully", data="")


@router.get("/{inventory_id}/batches/organization/{organization_id}", response_model=APIResponse[List[BatchResponse]])
def get_batches_route(
    inventory_id: str,
    organization_id: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    batches = get_batches_by_inventory_id(
        db=db,
        inventory_id=inventory_id,
        organization_id=organization_id,
        skip=skip,
        limit=limit
    )
    return success_response("Batches fetched successfully", batches)


@router.put("/batch/{batch_id}/organization/{organization_id}", response_model=APIResponse[BatchResponse])
def update_batch_route(
    batch_id: str,
    organization_id: str,
    payload: BatchUpdate,
    db: Session = Depends(get_db)
):
    result = update_batch(
        db=db,
        batch_id=batch_id,
        batch_data=payload,
        organization_id=organization_id
    )
    if not result:
        return not_found_response("Batch record not found", data="")
    return success_response("Batch updated successfully", result)


@router.delete("/batch/{batch_id}/organization/{organization_id}", response_model=APIResponse[str])
def delete_batch_route(
    batch_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    success = delete_batch(db=db, batch_id=batch_id, organization_id=organization_id)
    if not success:
        return not_found_response("Batch record not found", data="")
    return success_response("Batch deleted successfully", data="")


@router.get("/dropdown/medicines/organization/{organization_id}", response_model=APIResponse[List[MasterOptionDropdownResponse]])
def get_medicine_dropdown_route(
    organization_id: str,
    branch_id: str,
    db: Session = Depends(get_db)
):
    options = get_medicine_dropdown(db=db, organization_id=organization_id, branch_id=branch_id)
    return success_response("Medicine dropdown fetched successfully", options)


@router.get("/dropdown/suppliers/organization/{organization_id}", response_model=APIResponse[List[SupplierDropdownResponse]])
def get_supplier_dropdown_route(
    organization_id: str,
    branch_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    options = get_supplier_dropdown(db=db, organization_id=organization_id, branch_id=branch_id)
    return success_response("Supplier dropdown fetched successfully", options)

