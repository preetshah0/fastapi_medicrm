from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.patient import (
    NoteCreate, NoteUpdate, NoteResponse,
    ReportCreate, ReportUpdate, ReportResponse,
    PatientCreate, PatientUpdate, PatientResponse
)
from app.owner.controller.patient import (
    create_patient,
    get_patient,
    get_patient_by_id,
    get_patients_by_organization,
    update_patient,
    delete_patient,
    create_note,
    get_note,
    get_all_notes,
    get_notes_by_patient,
    update_note,
    delete_note,
    create_report,
    get_report,
    get_all_reports,
    get_reports_by_patient,
    update_report,
    delete_report,
)
from app.utils.auth_utils import get_current_user_id
from app.utils.ApiResponse import success_response, not_found_response, error_response

router = APIRouter(prefix="/owner/patients", tags=["patients"])


@router.post("/create", response_model=APIResponse[PatientResponse])
def create_patient_route(
    payload: PatientCreate,
    db: Session = Depends(get_db),
):


    result = create_patient(db=db, patient=payload)
    if not result:
        return error_response("Error creating patient or organization not found", data="")

    return success_response("Patient created successfully", result)


@router.get("/{patient_id}", response_model=APIResponse[PatientResponse])
def get_patient_route(
    patient_id: str,
    db: Session = Depends(get_db),
):
    result = get_patient_by_id(db=db, patient_id=patient_id)
    if not result:
        return not_found_response("Patient not found", data="")

    return success_response("Patient fetched successfully", result)


@router.get("/{organization_id}", response_model=APIResponse[list[PatientResponse]])
def get_patients_by_organization_route(
    organization_id: str,
    db: Session = Depends(get_db),
):
    result = get_patients_by_organization(db=db, organization_id=organization_id)
    if result is None:
        return not_found_response("Organization not found", data="")

    return success_response("Patients fetched successfully", result)


@router.get("/{ref_code}", response_model=APIResponse[PatientResponse])
def get_patient_by_ref_code_route(
    ref_code: str,
    db: Session = Depends(get_db),
):
    result = get_patient(db=db, ref_code=ref_code)
    if not result:
        return not_found_response("Patient not found", data="")

    return success_response("Patient fetched successfully", result)


@router.put("/{patient_id}", response_model=APIResponse[PatientResponse])
def update_patient_route(
    patient_id: str,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
):
    result = update_patient(db=db, patient_id=patient_id, patient=payload)
    if not result:
        return not_found_response("Patient not found", data="")

    return success_response("Patient updated successfully", result)


@router.delete("/{patient_id}")
def delete_patient_route(
    patient_id: str,
    db: Session = Depends(get_db),
):
    result = delete_patient(db=db, patient_id=patient_id)
    if not result:
        return not_found_response("Patient not found", data="")

    return success_response("Patient deleted successfully", data="")


notes_router = APIRouter(prefix="/owner/notes", tags=["notes"])


@notes_router.post("/create", response_model=APIResponse[NoteResponse])
def create_note_route(
    payload: NoteCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = create_note(db=db, note=payload, user_id=user_id)
    if not result:
        return not_found_response("Patient not found", data="")

    return success_response("Note created successfully", result)


@notes_router.get("/{note_id}", response_model=APIResponse[NoteResponse])
def get_note_route(
    note_id: str,
    db: Session = Depends(get_db),
):
    result = get_note(db=db, note_id=note_id)
    if not result:
        return not_found_response("Note not found", data="")

    return success_response("Note fetched successfully", result)


@notes_router.get("/{patient_id}", response_model=APIResponse[list[NoteResponse]])
def get_patient_notes_route(
    patient_id: str,
    db: Session = Depends(get_db),
):
    result = get_notes_by_patient(db=db, patient_id=patient_id)
    if result is None:
        return not_found_response("Patient not found", data="")

    return success_response("Notes fetched successfully", result)


@notes_router.get("", response_model=APIResponse[list[NoteResponse]])
def get_all_notes_route(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = get_all_notes(db=db, user_id=user_id)
    if not result:
        return not_found_response("Notes not found", data="")

    return success_response("Notes fetched successfully", result)


@notes_router.put("/{note_id}", response_model=APIResponse[NoteResponse])
def update_note_route(
    note_id: str,
    payload: NoteUpdate,
    db: Session = Depends(get_db),
):
    result = update_note(db=db, note_id=note_id, note=payload)
    if not result:
        return not_found_response("Note not found", data="")

    return success_response("Note updated successfully", result)


@notes_router.delete("/{note_id}")
def delete_note_route(
    note_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    result = delete_note(db=db, note_id=note_id)
    if not result:
        return not_found_response("Note not found", data="")

    return success_response("Note deleted successfully", data="")


reports_router = APIRouter(prefix="/owner/reports", tags=["reports"])


@reports_router.post("/create", response_model=APIResponse[ReportResponse])
def create_report_route(
    payload: ReportCreate,
    db: Session = Depends(get_db),
):
    result = create_report(db=db, report=payload)
    if not result:
        return not_found_response("Patient not found", data="")

    return success_response("Report created successfully", result)


@reports_router.get("/{report_id}", response_model=APIResponse[ReportResponse])
def get_report_route(
    report_id: str,
    db: Session = Depends(get_db),
):
    result = get_report(db=db, report_id=report_id)
    if not result:
        return not_found_response("Report not found", data="")

    return success_response("Report fetched successfully", result)


@reports_router.get("/patient/{patient_id}", response_model=APIResponse[list[ReportResponse]])
def get_patient_reports_route(
    patient_id: str,
    db: Session = Depends(get_db),
):
    result = get_reports_by_patient(db=db, patient_id=patient_id)
    if result is None:
        return not_found_response("Patient not found", data="")

    return success_response("Reports fetched successfully", result)


@reports_router.get("/all", response_model=APIResponse[list[ReportResponse]])
def get_all_reports_route(
    db: Session = Depends(get_db),
):
    result = get_all_reports(db=db)
    if not result:
        return not_found_response("Reports not found", data="")

    return success_response("Reports fetched successfully", result)


@reports_router.put("/{report_id}", response_model=APIResponse[ReportResponse])
def update_report_route(
    report_id: str,
    payload: ReportUpdate,
    db: Session = Depends(get_db),
):
    result = update_report(db=db, report_id=report_id, report=payload)
    if not result:
        return not_found_response("Report not found", data="")

    return success_response("Report updated successfully", result)


@reports_router.delete("/{report_id}")
def delete_report_route(
    report_id: str,
    db: Session = Depends(get_db),
):
    result = delete_report(db=db, report_id=report_id)
    if not result:
        return not_found_response("Report not found", data="")

    return success_response("Report deleted successfully", data="")
