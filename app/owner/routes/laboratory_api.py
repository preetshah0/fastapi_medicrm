from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.labs import (
    LabCreate,
    LabUpdate,
    LabResponse,
    LabEnumResponse,
    LabVisitCreate,
    LabVisitResponse
)
from app.db.schemas.master_options import MasterOptionDropdownResponse
from app.owner.controller.laboratory import (
    create_laboratory,
    update_laboratory,
    delete_laboratory,
    get_laboratory,
    get_laboratories_by_branch,
    create_lab_visit,
    get_lab_visits,
    get_lab_type_dropdown,
    get_laboratory_facility_type,
)
from app.utils.ApiResponse import success_response, error_response, not_found_response

router = APIRouter(prefix="/owner/laboratories", tags=["laboratories"])

@router.get("/facility-types", response_model=APIResponse[list[LabEnumResponse]])
def get_laboratory_facility_type_route():
    result = get_laboratory_facility_type()
    return success_response("Laboratory facility types fetched successfully", result)

@router.get("/lab-types/{organization_id}", response_model=APIResponse[list[MasterOptionDropdownResponse]])
def get_lab_type_dropdown_route(organization_id: str, db: Session = Depends(get_db)):
    result = get_lab_type_dropdown(db=db, organization_id=organization_id)
    return success_response("Lab types fetched successfully", result)

@router.post("/create/{branch_id}", response_model=APIResponse[LabResponse])
def create_laboratory_route(branch_id: str, payload: LabCreate, db: Session = Depends(get_db)):
    result = create_laboratory(db=db, branch_id=branch_id, lab_data=payload)
    if not result:
        return error_response("Failed to create laboratory", data="")
        
    return success_response("Laboratory created successfully", result)

@router.put("/{lab_id}", response_model=APIResponse[LabResponse])
def update_laboratory_route(lab_id: str, payload: LabUpdate, db: Session = Depends(get_db)):
    result = update_laboratory(db=db, lab_id=lab_id, lab_data=payload)
    if not result:
        return not_found_response("Laboratory not found or failed to update", data="")
    return success_response("Laboratory updated successfully", result)

@router.delete("/{lab_id}")
def delete_laboratory_route(lab_id: str, db: Session = Depends(get_db)):
    result = delete_laboratory(db=db, lab_id=lab_id)
    if not result:
        return not_found_response("Laboratory not found", data="")
    return success_response("Laboratory deleted successfully", data="")

@router.get("/branch/{branch_id}", response_model=APIResponse[list[LabResponse]])
def get_laboratories_by_branch_route(branch_id: str, db: Session = Depends(get_db)):
    result = get_laboratories_by_branch(db=db, branch_id=branch_id)
    if not result:
        return not_found_response("Laboratories not found for this branch", data="")
    return success_response("Laboratories fetched successfully", result)

@router.get("/{lab_id}", response_model=APIResponse[LabResponse])
def get_laboratory_route(lab_id: str, db: Session = Depends(get_db)):
    result = get_laboratory(db=db, lab_id=lab_id)
    if not result:
        return not_found_response("Laboratory not found", data="")
    return success_response("Laboratory fetched successfully", result)

@router.post("/{lab_id}/visit", response_model=APIResponse[LabVisitResponse])
def create_lab_visit_route(lab_id: str, payload: LabVisitCreate, db: Session = Depends(get_db)):
    db_lab = get_laboratory(db=db, lab_id=lab_id)
    if not db_lab:
        return not_found_response("Laboratory not found for this visit", data="")

    result = create_lab_visit(db=db, lab_id=lab_id, visit_data=payload)
    if not result:
        return error_response("Failed to create laboratory visit", data="")
    return success_response("Laboratory visit created successfully", result)

@router.get("/{lab_id}/visits", response_model=APIResponse[list[LabVisitResponse]])
def get_lab_visits_route(lab_id: str, db: Session = Depends(get_db)):
    result = get_lab_visits(db=db, lab_id=lab_id)
    if not result:
        return not_found_response("Laboratory visits not found", data="")
    return success_response("Laboratory visits fetched successfully", result)
