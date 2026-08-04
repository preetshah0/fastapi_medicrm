from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.db.schemas import APIResponse
from app.Enum.AppointmentStatus import AppointmentStatus
from app.db.schemas.appointments import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentStatusUpdate,
    AppointmentResponse,
    AppointmentSlotResponse,
    AppointmentDurationOptionResponse,
)
from app.Enum.AppointmentDuration import AppointmentDuration
from app.owner.controller.appointment import (
    create_appointment,
    get_appointment_by_id,
    get_all_appointments,
    get_appointments_by_patient,
    get_appointment_duration_options,
    get_available_appointment_slots_for_branch,
    update_appointment,
    update_appointment_status,
    delete_appointment,
)
from app.utils.ApiResponse import success_response, not_found_response, error_response

router = APIRouter(prefix="/owner/appointments", tags=["appointments"])


@router.post("/create", response_model=APIResponse[AppointmentResponse])
def create_appointment_route(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
):
    result = create_appointment(db=db, payload=payload)
    if not result:
        return error_response("Error creating appointment. Verify branch, doctor, and patient IDs.", data="")
    return success_response("Appointment created and logged successfully", result)


@router.get("/all", response_model=APIResponse[List[AppointmentResponse]])
def get_all_appointments_route(
    db: Session = Depends(get_db),
):
    result = get_all_appointments(db=db)
    return success_response("Appointments fetched successfully", result)


@router.get("/slots", response_model=APIResponse[List[AppointmentSlotResponse]])
def get_available_appointment_slots_route(
    branch_id: str,
    doctor_id: str,
    appointment_date: str,
    duration_minutes: AppointmentDuration = AppointmentDuration.FIFTEEN,
    db: Session = Depends(get_db),
):
    try:
        appointment_date_parsed = datetime.fromisoformat(appointment_date).date()
    except Exception:
        return error_response("Invalid appointment_date format. Use YYYY-MM-DD.", data="")

    result = get_available_appointment_slots_for_branch(
        db=db,
        branch_id=branch_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date_parsed,
        duration_minutes=int(duration_minutes),
    )
    if result is None:
        return error_response("Branch not found.", data="")
    return success_response("Available slots fetched successfully", result)


@router.get("/durations", response_model=APIResponse[List[AppointmentDurationOptionResponse]])
def get_appointment_duration_options_route(
    db: Session = Depends(get_db),
):
    result = get_appointment_duration_options()
    return success_response("Appointment duration options fetched successfully", result)


@router.get("/{appointment_id}", response_model=APIResponse[AppointmentResponse])
def get_appointment_route(
    appointment_id: str,
    db: Session = Depends(get_db),
):
    result = get_appointment_by_id(db=db, appointment_id=appointment_id)
    if not result:
        return not_found_response("Appointment not found", data="")
    return success_response("Appointment fetched successfully", result)


@router.get("/patient/{patient_id}", response_model=APIResponse[List[AppointmentResponse]])
def get_patient_appointments_route(
    patient_id: str,
    db: Session = Depends(get_db),
):
    result = get_appointments_by_patient(db=db, patient_id=patient_id)
    return success_response("Patient appointments fetched successfully", result)


@router.put("/{appointment_id}", response_model=APIResponse[AppointmentResponse])
def update_appointment_route(
    appointment_id: str,
    payload: AppointmentUpdate,
    db: Session = Depends(get_db),
):
    existing_appointment = get_appointment_by_id(db=db, appointment_id=appointment_id)
    if existing_appointment and existing_appointment.status == AppointmentStatus.OVERDUE.value:
        return error_response("Cannot update an overdue appointment", data="")

    result = update_appointment(db=db, appointment_id=appointment_id, payload=payload)
    if not result:
        return not_found_response("Appointment not found", data="")
    return success_response("Appointment updated successfully", result)


@router.patch("/{appointment_id}/status", response_model=APIResponse[AppointmentResponse])
def update_appointment_status_route(
    appointment_id: str,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
):
    existing_appointment = get_appointment_by_id(db=db, appointment_id=appointment_id)
    if existing_appointment and existing_appointment.status == AppointmentStatus.OVERDUE.value:
        return error_response("Cannot change status of an overdue appointment", data="")

    result = update_appointment_status(db=db, appointment_id=appointment_id, payload=payload)
    if not result:
        return not_found_response("Appointment not found", data="")
    return success_response("Appointment status updated and logged successfully", result)


@router.delete("/{appointment_id}")
def delete_appointment_route(
    appointment_id: str,
    db: Session = Depends(get_db),
):
    result = delete_appointment(db=db, appointment_id=appointment_id)
    if not result:
        return not_found_response("Appointment not found", data="")
    return success_response("Appointment deleted successfully", data="")
