from typing import List, Optional
from datetime import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.prescriptions import (
    PrescriptionCreate,
    PrescriptionUpdate,
    PrescriptionResponse,
    PrescriptionMedicationCreate,
    PrescriptionMedicationUpdate,
    PrescriptionMedicationResponse,
    BranchDropdownResponse,
    DoctorDropdownResponse,
    PatientDropdownResponse,
    MedicationDropdownResponse,
    FollowupDurationOptionResponse,
)
from app.owner.controller.prescription import (
    create_prescription,
    create_medication,
    get_prescriptions,
    get_prescription_by_id,
    update_prescription,
    update_medications,
    delete_prescription,
    delete_medication,
    get_branch_dropdown,
    get_doctor_dropdown,
    get_patient_dropdown,
    update_prescription_status,
    toggle_followup,
    get_medication_names,
    get_followup_duration_types,
    calculate_followup_end_time_controller,
)
from app.utils.ApiResponse import success_response, error_response, not_found_response

router = APIRouter(prefix="/owner/prescriptions", tags=["prescriptions"])


@router.post("/create", response_model=APIResponse[PrescriptionResponse])
def create_prescription_route(
    payload: PrescriptionCreate,
    db: Session = Depends(get_db)
):
    result = create_prescription(db=db, prescription_data=payload)
    return success_response("Prescription created successfully", result)


@router.get("/organization/{organization_id}", response_model=APIResponse[List[PrescriptionResponse]])
def get_prescriptions_route(
    organization_id: str,
    db: Session = Depends(get_db)
):
    results = get_prescriptions(db=db, organization_id=organization_id)
    return success_response("Prescriptions fetched successfully", results)


@router.get("/{prescription_id}/organization/{organization_id}", response_model=APIResponse[PrescriptionResponse])
def get_prescription_route(
    prescription_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    result = get_prescription_by_id(db=db, prescription_id=prescription_id, organization_id=organization_id)
    if not result:
        return not_found_response("Prescription not found", data="")
    return success_response("Prescription fetched successfully", result)


@router.put("/{prescription_id}/organization/{organization_id}", response_model=APIResponse[PrescriptionResponse])
def update_prescription_route(
    prescription_id: str,
    organization_id: str,
    payload: PrescriptionUpdate,
    db: Session = Depends(get_db)
):
    result = update_prescription(
        db=db,
        prescription_id=prescription_id,
        prescription_data=payload,
        organization_id=organization_id
    )
    if not result:
        return not_found_response("Prescription not found", data="")
    return success_response("Prescription updated successfully", result)


@router.delete("/{prescription_id}/organization/{organization_id}", response_model=APIResponse[str])
def delete_prescription_route(
    prescription_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    success = delete_prescription(db=db, prescription_id=prescription_id, organization_id=organization_id)
    if not success:
        return not_found_response("Prescription not found", data="")
    return success_response("Prescription deleted successfully", data="")



@router.post("/{prescription_id}/medication/organization/{organization_id}", response_model=APIResponse[PrescriptionMedicationResponse])
def create_medication_route(
    prescription_id: str,
    organization_id: str,
    payload: PrescriptionMedicationCreate,
    db: Session = Depends(get_db)
):
    result = create_medication(
        db=db,
        prescription_id=prescription_id,
        medication_data=payload,
        organization_id=organization_id
    )
    if not result:
        return not_found_response("Prescription not found", data="")
    return success_response("Medication added to prescription successfully", result)


@router.put("/medication/{medication_id}/organization/{organization_id}", response_model=APIResponse[PrescriptionMedicationResponse])
def update_medication_route(
    medication_id: str,
    organization_id: str,
    payload: PrescriptionMedicationUpdate,
    db: Session = Depends(get_db)
):
    result = update_medications(
        db=db,
        medication_id=medication_id,
        medication_data=payload,
        organization_id=organization_id
    )
    if not result:
        return not_found_response("Medication line item not found", data="")
    return success_response("Medication updated successfully", result)


@router.delete("/medication/{medication_id}/organization/{organization_id}", response_model=APIResponse[str])
def delete_medication_route(
    medication_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    success = delete_medication(db=db, medication_id=medication_id, organization_id=organization_id)
    if not success:
        return not_found_response("Medication line item not found", data="")
    return success_response("Medication deleted successfully", data="")

@router.patch("/{prescription_id}/status/organization/{organization_id}", response_model=APIResponse[bool])
def update_prescription_status_route(
    prescription_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    success = update_prescription_status(db=db, prescription_id=prescription_id, organization_id=organization_id)
    if not success:
        return error_response("Prescription cannot be finalized or it is already finalized", data=False)
    return success_response("Prescription finalized successfully", True)


@router.patch("/{prescription_id}/followup/organization/{organization_id}", response_model=APIResponse[PrescriptionResponse])
def toggle_followup_route(
    prescription_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    result = toggle_followup(db=db, prescription_id=prescription_id, organization_id=organization_id)
    if not result:
        return not_found_response("Prescription not found", data="")
    return success_response("Follow-up status toggled successfully", result)



@router.get("/branches/organization/{organization_id}", response_model=APIResponse[List[BranchDropdownResponse]])
def get_branch_dropdown_route(
    organization_id: str,
    db: Session = Depends(get_db)
):
    options = get_branch_dropdown(db=db, organization_id=organization_id)
    return success_response("Branch dropdown fetched successfully", options)


@router.get("/doctors/organization/{organization_id}", response_model=APIResponse[List[DoctorDropdownResponse]])
def get_doctor_dropdown_route(
    organization_id: str,
    db: Session = Depends(get_db)
):
    options = get_doctor_dropdown(db=db, organization_id=organization_id)
    return success_response("Doctor dropdown fetched successfully", options)


@router.get("/patients/organization/{organization_id}", response_model=APIResponse[List[PatientDropdownResponse]])
def get_patient_dropdown_route(
    organization_id: str,
    db: Session = Depends(get_db)
):
    options = get_patient_dropdown(db=db, organization_id=organization_id)
    return success_response("Patient dropdown fetched successfully", options)


@router.get("/medications/organization/{organization_id}", response_model=APIResponse[List[MedicationDropdownResponse]])
def get_medication_names_route(
    organization_id: str,
    branch_id: str,
    db: Session = Depends(get_db)
):
    options = get_medication_names(db=db, organization_id=organization_id, branch_id=branch_id)
    return success_response("Medication dropdown fetched successfully", options)


@router.get("/followup-durations", response_model=APIResponse[List[FollowupDurationOptionResponse]])
def get_followup_duration_types_route():
    options = get_followup_duration_types()
    return success_response("Follow-up duration options fetched successfully", options)


@router.get("/calculate-followup-end-time", response_model=APIResponse[Optional[time]])
def calculate_followup_end_time_route(
    followup_time: Optional[time] = None,
    followup_duration: Optional[int] = None,
):
    result = calculate_followup_end_time_controller(followup_time, followup_duration)
    if result is None:
        return error_response("Both followup_time and followup_duration are required", data=None)

    return success_response("Follow-up end time calculated successfully", result)
