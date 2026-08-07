from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.suppliers import (
    SupplierCreate,
    SupplierUpdate,
    SupplierResponse,
    SupplierVisitCreate,
    SupplierVisitResponse
)
from app.model.Supplier import Supplier, SupplierVisit
from app.owner.controller.supplier import (
    create_supplier,
    update_supplier,
    delete_supplier,
    get_suppliers,
    get_suppliers_by_branch,
    create_supplier_visit,
    get_supplier_visits,
    generate_supplier_batch_number
)
from app.utils.ApiResponse import success_response, error_response, not_found_response

router = APIRouter(prefix="/owner/suppliers", tags=["suppliers"])

from app.model.MedicalRep import MedicalReps
from app.model.Branch import Branch
from app.Enum.SupplierType import SupplierType

@router.post("/create/{branch_id}", response_model=APIResponse[SupplierResponse])
def create_supplier_route(branch_id: str, payload: SupplierCreate, db: Session = Depends(get_db)):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        return error_response("Branch not found", data="")

    if payload.type == SupplierType.MEDICAL_REPRESENTATIVE:
        if not payload.reps_id:
            return error_response("Medical Representative ID is required", data="")
        
        db_reps = db.query(MedicalReps).filter(MedicalReps.id == payload.reps_id).first()
        if not db_reps:
            return error_response("Medical Representative not found", data="")

    result = create_supplier(db=db, branch_id=branch_id, supplier_data=payload)
    if not result:
        return error_response("Failed to create supplier", data="")
        
    return success_response("Supplier created successfully", result)

@router.put("/{supplier_id}", response_model=APIResponse[SupplierResponse])
def update_supplier_route(supplier_id: str, payload: SupplierUpdate, db: Session = Depends(get_db)):
    db_supplier = get_suppliers(db, supplier_id)
    if not db_supplier:
        return not_found_response("Supplier not found", data="")


    if db_supplier.type == SupplierType.MEDICAL_REPRESENTATIVE.value:
        if not payload.reps_id:
            return error_response("Medical Representative ID is required", data="")
            
        db_reps = db.query(MedicalReps).filter(MedicalReps.id == payload.reps_id).first()
        if not db_reps:
            return error_response("Medical Representative not found", data="")

    result = update_supplier(db=db, supplier_id=supplier_id, supplier_data=payload)
    if not result:
        return error_response("Failed to update supplier", data="")
    return success_response("Supplier updated successfully", result)

@router.delete("/{supplier_id}")
def delete_supplier_route(supplier_id: str, db: Session = Depends(get_db)):
    result = delete_supplier(db=db, supplier_id=supplier_id)
    if not result:
        return not_found_response("Supplier not found", data="")
    return success_response("Supplier deleted successfully", data="")

@router.get("/branch/{branch_id}", response_model=APIResponse[list[SupplierResponse]])
def get_suppliers_by_branch_route(branch_id: str, db: Session = Depends(get_db)):
    result = get_suppliers_by_branch(db=db, branch_id=branch_id)
    if not result:
        return not_found_response("Suppliers not found", data="")
    return success_response("Suppliers fetched successfully", result)

@router.get("/{supplier_id}", response_model=APIResponse[SupplierResponse])
def get_supplier_route(supplier_id: str, db: Session = Depends(get_db)):
    result = get_suppliers(db=db, supplier_id=supplier_id)
    if not result:
        return not_found_response("Supplier not found", data="")
    return success_response("Supplier fetched successfully", result)

@router.post("/{supplier_id}/visit", response_model=APIResponse[SupplierVisitResponse])
def create_supplier_visit_route(supplier_id: str, payload: SupplierVisitCreate, db: Session = Depends(get_db)):
    result = create_supplier_visit(db=db, supplier_id=supplier_id, visit_data=payload)
    if not result:
        return error_response("Supplier not found for this visit", data="")
    return success_response("Supplier Visit created successfully", result)

@router.get("/{supplier_id}/visits", response_model=APIResponse[list[SupplierVisitResponse]])
def get_supplier_visits_route(supplier_id: str, db: Session = Depends(get_db)):
    result = get_supplier_visits(db=db, supplier_id=supplier_id)
    if not result:
        return not_found_response("Supplier Visits not found", data="")
    return success_response("Supplier Visits fetched successfully", result)
