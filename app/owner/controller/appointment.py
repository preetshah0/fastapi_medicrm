from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, time
from app.model.appointments import Appointment
from app.model.Branch import Branch
from app.model.User import User
from app.model.Patient import Patient
from app.db.schemas.appointments import AppointmentCreate, AppointmentUpdate, AppointmentStatusUpdate
from app.Enum.AppointmentDuration import AppointmentDuration
from app.Enum.AppointmentStatus import AppointmentStatus
from app.services.appointment_service import (
    calculate_end_time,
    get_available_appointment_slots,
    log_patient_appointment,
    log_patient_visit,
    mark_overdue_appointments,
)


def create_appointment(db: Session, payload: AppointmentCreate) -> Appointment:
    mark_overdue_appointments(db)

    branch = db.query(Branch).filter(Branch.id == payload.branch_id).first()
    if not branch:
        return None

    doctor = db.query(User).filter(User.id == payload.doctor_id).first()
    if not doctor:
        return None

    patient = db.query(Patient).filter(Patient.id == payload.patient_id).first()
    if not patient:
        return None

    end_time = calculate_end_time(payload.start_time, payload.duration_minutes.value)

    appointment = Appointment(
        branch_id=payload.branch_id,
        doctor_id=payload.doctor_id,
        patient_id=payload.patient_id,
        appointment_date=payload.appointment_date,
        location=branch.name,
        start_time=payload.start_time,
        end_time=end_time,
        status=payload.status.value,
        type=payload.type.value,
        duration_minutes=payload.duration_minutes.value,
        notes=payload.notes,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    
    log_patient_appointment(db, appointment)

    db.refresh(appointment)
    return appointment


def get_appointment_by_id(db: Session, appointment_id: str) -> Appointment:
    mark_overdue_appointments(db)
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def get_all_appointments(db: Session):
    mark_overdue_appointments(db)
    return db.query(Appointment).all()


def get_appointments_by_patient(db: Session, patient_id: str):
    mark_overdue_appointments(db)
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()


def update_appointment(db: Session, appointment_id: str, payload: AppointmentUpdate) -> Appointment:
    mark_overdue_appointments(db)

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        return None

    if appointment.status == AppointmentStatus.OVERDUE.value:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            if hasattr(value, "value"):
                setattr(appointment, key, value.value)
            else:
                setattr(appointment, key, value)

    if appointment.start_time is not None and appointment.duration_minutes is not None:
        appointment.end_time = calculate_end_time(appointment.start_time, appointment.duration_minutes)

    db.commit()
    db.refresh(appointment)

    # Automatically update linked PatientAppointment log
    log_patient_appointment(db, appointment)

    db.refresh(appointment)
    return appointment


def get_available_appointment_slots_for_branch(
    db: Session,
    branch_id: str,
    doctor_id: Optional[str],
    appointment_date: date,
    duration_minutes: AppointmentDuration = AppointmentDuration.FIFTEEN,
):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        return None
    return get_available_appointment_slots(
        db=db,
        branch_id=branch_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        duration_minutes=duration_minutes,
    )


def get_appointment_duration_options() -> list[dict[str, object]]:
    return [
        {
            "value": duration.value,
            "label": duration.label,
        }
        for duration in AppointmentDuration
    ]


def update_appointment_status(db: Session, appointment_id: str, payload: AppointmentStatusUpdate) -> Appointment:
    mark_overdue_appointments(db)

    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        return None

    if appointment.status == AppointmentStatus.OVERDUE.value:
        return None

    appointment.status = payload.status.value
    db.commit()
    db.refresh(appointment)

    # Sync patient appointment log
    log_patient_appointment(db, appointment)

    if payload.status == AppointmentStatus.COMPLETED:
        if payload.payment_details:
            log_patient_visit(
                db=db,
                appointment=appointment,
                patient=payload.payment_details
            )

    db.refresh(appointment)
    return appointment


def delete_appointment(db: Session, appointment_id: str) -> Appointment:
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        return None

    db.delete(appointment)
    db.commit()
    return appointment
