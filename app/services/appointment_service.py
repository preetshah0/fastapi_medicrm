from app.db.schemas import PatientVisitCreate
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta
from typing import Optional, List

from app.model.Appointment import Appointment
from app.model.Branch import Branch
from app.model.Patient import PatientAppointment, PatientVisit
from app.Enum.AppointmentStatus import AppointmentStatus
from app.Enum.AppointmentDuration import AppointmentDuration
from app.Enum.PatientVisitPaymentStatus import PatientVisitPaymentStatus


def log_patient_appointment(db: Session, appointment: Appointment):
    existing_log = (
        db.query(PatientAppointment)
        .filter(PatientAppointment.appointment_id == appointment.id)
        .first()
    )

    if existing_log:
        existing_log.patient_id = appointment.patient_id
        existing_log.location = appointment.location or ""
        existing_log.appointment_date = appointment.appointment_date
        existing_log.appointment_time = appointment.start_time
        existing_log.duration_minutes = appointment.duration_minutes
        db.commit()
        db.refresh(existing_log)
        return existing_log
    else:
        new_log = PatientAppointment(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            location=appointment.location or "",
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.start_time,
            duration_minutes=appointment.duration_minutes,
        )
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        return new_log


def log_patient_visit(
    db: Session,
    appointment: Appointment,
    patient:PatientVisitCreate
):

    if str(appointment.status).lower() != AppointmentStatus.COMPLETED.value.lower():
        return None

    now = datetime.now()

    existing_visit = (
        db.query(PatientVisit)
        .filter(PatientVisit.appointment_id == appointment.id)
        .first()
    )

    if existing_visit:
        existing_visit.visited_date = now.date()
        existing_visit.visit_time = now.time()
        existing_visit.amount_charged = patient.amount_charged
        existing_visit.payment_mode = patient.payment_mode
        existing_visit.payment_status = patient.payment_status
        existing_visit.notes = appointment.notes
        db.commit()
        db.refresh(existing_visit)
        return existing_visit
    else:
        new_visit = PatientVisit(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            visited_date=now.date(),
            visit_time=now.time(),
            amount_charged=patient.amount_charged,
            payment_mode=patient.payment_mode,
            payment_status=patient.payment_status,
            notes=appointment.notes,
        )
        db.add(new_visit)
        db.commit()
        db.refresh(new_visit)
        return new_visit

def calculate_end_time(start_time: time, duration_minutes: int) -> time:
    return (datetime.combine(date.today(), start_time) + timedelta(minutes=duration_minutes)).time()


def mark_overdue_appointments(db: Session) -> int:
    today = date.today()
    overdue_appointments = (
        db.query(Appointment)
        .filter(Appointment.appointment_date < today)
        .filter(Appointment.status == AppointmentStatus.SCHEDULED.value)
        .all()
    )

    for appointment in overdue_appointments:
        appointment.status = AppointmentStatus.OVERDUE.value

    if overdue_appointments:
        db.commit()

    return len(overdue_appointments)


def dynamic_slots(opening_time: time, closing_time: time) -> List[dict[str, str]] | None:
    if opening_time is None or closing_time is None:
        return None

    if opening_time >= closing_time:
        return None

    slots: List[dict[str, str]] = []
    current = datetime.combine(date.today(), opening_time)
    end_boundary = datetime.combine(date.today(), closing_time)

    while current <= end_boundary:
        slots.append({
            "value": current.time().strftime("%H:%M:%S"),
            "label": current.time().strftime("%I:%M %p"),
        })
        current += timedelta(minutes=15)

    return slots


def is_slot_blocked(
    db: Session,
    branch_id: str,
    doctor_id: str,
    appointment_date: date,
    slot_time: time,
    duration_minutes: int,
) -> bool:
    slot_start = datetime.combine(appointment_date, slot_time)
    slot_end = slot_start + timedelta(minutes=duration_minutes)

    if appointment_date == date.today() and slot_start < datetime.now():
        return True

    if not branch_id or not doctor_id:
        return False

    existing_appointments = (
        db.query(Appointment)
        .filter(Appointment.branch_id == branch_id)
        .filter(Appointment.doctor_id == doctor_id)
        .filter(Appointment.appointment_date == appointment_date)
        .filter(Appointment.status == AppointmentStatus.SCHEDULED.value)
        .all()
    )

    for appointment in existing_appointments:
        if not appointment.start_time:
            continue

        existing_end_time = (
            appointment.end_time
            if appointment.end_time is not None
            else calculate_end_time(appointment.start_time, appointment.duration_minutes)
        )

        if appointment.start_time < slot_end and existing_end_time > slot_time:
            return True

    return False


def get_available_appointment_slots(
    db: Session,
    branch_id: str,
    doctor_id: str,
    appointment_date: date,
    duration_minutes: AppointmentDuration ,
) :
    if not appointment_date or duration_minutes <= 0:
        return None

    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        return None

    opening_time = branch.opening_time
    closing_time = branch.closing_time
    if opening_time is None or closing_time is None:
        return None

    if opening_time >= closing_time:
        return None

    last_allowed_slot = (datetime.combine(date.today(), closing_time) - timedelta(minutes=duration_minutes)).time()

    if last_allowed_slot < opening_time:
        return None

    slots = dynamic_slots(opening_time, last_allowed_slot)
    if slots is None:
        return None
    available_slots: List[dict[str, object]] = []

    for slot in slots:
        slot_time = datetime.strptime(slot["value"], "%H:%M:%S").time()
        available_slots.append({
            "value": slot["value"],
            "label": slot["label"],
            "disabled": is_slot_blocked(
                db,
                branch_id,
                doctor_id,
                appointment_date,
                slot_time,
                duration_minutes,
            ),
        })

    return available_slots
