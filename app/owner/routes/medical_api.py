from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.medical_reps import (
    MedicalRepsCreate,
    MedicalRepsUpdate,
    MedicalRepsResponse,
    MedicalRepVisitCreate,
    MedicalRepVisitResponse
)
from app.model.MedicalRep import MedicalReps
from app.owner.controller.medical import (
    create_medical_representatives,
    update_medical_representatives,
    delete_medical_representatives,
    get_medical_representatives,
    create_mr_visit,
    get_mr_visit,
    get_product
)
from app.utils.ApiResponse import success_response, error_response, not_found_response
from app.utils.auth_utils import require_permission

router = APIRouter(prefix="/owner/medical-reps", tags=["medical-reps"])

@router.post(
    "/create/{branch_id}",
    dependencies=[Depends(require_permission("medical_representatives", action="create"))],
    response_model=APIResponse[MedicalRepsResponse],
)
def create_medical_rep_route(branch_id: str, payload: MedicalRepsCreate, db: Session = Depends(get_db)):
    db_email = db.query(MedicalReps).filter(
        MedicalReps.company_email == payload.company_email,
        MedicalReps.branch_id == branch_id
    ).first()

    if db_email:
        return error_response("Medical Representative already existed for this branch", data="")
    
    result = create_medical_representatives(db=db, branch_id=branch_id, medical_rep_data=payload)
    if not result:
        return error_response("Branch not found", data="")
        
    return success_response("Medical Representative created successfully", result)

@router.put(
    "/{medical_rep_id}",
    dependencies=[Depends(require_permission("medical_representatives", action="edit"))],
    response_model=APIResponse[MedicalRepsResponse],
)
def update_medical_rep_route(medical_rep_id: str, payload: MedicalRepsUpdate, db: Session = Depends(get_db)):
    existing_rep = db.query(MedicalReps).filter(MedicalReps.id == medical_rep_id).first()
    if not existing_rep:
        return not_found_response("Medical Representative not found", data="")

    if payload.company_email:
        db_email = db.query(MedicalReps).filter(
            MedicalReps.company_email == payload.company_email,
            MedicalReps.branch_id == existing_rep.branch_id,
            MedicalReps.id != medical_rep_id
        ).first()
        if db_email:
            return error_response("Medical Representative already existed for this branch", data="")

    result = update_medical_representatives(db=db, medical_rep_id=medical_rep_id, medical_rep_data=payload)
    if not result:
        return not_found_response("Medical Representative not found", data="")
    return success_response("Medical Representative updated successfully", result)

@router.delete(
    "/{medical_rep_id}",
    dependencies=[Depends(require_permission("medical_representatives", action="delete"))],
)
def delete_medical_rep_route(medical_rep_id: str, db: Session = Depends(get_db)):
    result = delete_medical_representatives(db=db, medical_rep_id=medical_rep_id)
    if not result:
        return not_found_response("Medical Representative not found", data="")
    return success_response("Medical Representative deleted successfully", data="")

@router.get(
    "/branch/{branch_id}",
    dependencies=[Depends(require_permission("medical_representatives", action="view"))],
    response_model=APIResponse[list[MedicalRepsResponse]],
)
def get_medical_reps_by_branch_route(branch_id: str, db: Session = Depends(get_db)):
    result = get_medical_representatives(db=db, branch_id=branch_id)
    if not result:
        return not_found_response("Medical Representatives not found", data="")
    return success_response("Medical Representatives fetched successfully", result)

@router.post(
    "/{medical_rep_id}/visit",
    dependencies=[Depends(require_permission("medical_representatives", action="create"))],
    response_model=APIResponse[MedicalRepVisitResponse],
)
def create_mr_visit_route(medical_rep_id: str, payload: MedicalRepVisitCreate, db: Session = Depends(get_db)):
    result = create_mr_visit(db=db, medical_rep_id=medical_rep_id, mr_visit_data=payload)
    if not result:
        return not_found_response("MR Visit not found", data="")
    
    return success_response("MR Visit created successfully", result)

@router.get(
    "/{medical_rep_id}/visits",
    dependencies=[Depends(require_permission("medical_representatives", action="view"))],
    response_model=APIResponse[list[MedicalRepVisitResponse]],
)
def get_mr_visits_route(medical_rep_id: str, db: Session = Depends(get_db)):
    result = get_mr_visit(db=db, medical_rep_id=medical_rep_id)
    if not result:
        return not_found_response("MR Visits not found", data="")
    return success_response("MR Visits fetched successfully", result)

@router.get(
    "/{medical_rep_id}/products",
    dependencies=[Depends(require_permission("medical_representatives", action="view"))],
    response_model=APIResponse[list[str]],
)
def get_products_by_company_route(medical_rep_id: str, db: Session = Depends(get_db)):
    result = get_product(db=db, medical_rep_id=medical_rep_id)
    if not result:
        return not_found_response("Company products not found", data="")
    return success_response("Company products fetched successfully", result)

