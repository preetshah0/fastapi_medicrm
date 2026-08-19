from datetime import datetime, date, time
from typing import Optional
from sqlalchemy.orm import Session
from app.model.FollowUp import FollowUp
from app.model.Appointment import Appointment
from app.Enum.FollowupStatus import FollowupStatus
from app.Enum.FollowupVisitStatus import FollowupVisitStatus
from app.Enum.AppointmentStatus import AppointmentStatus
from app.services.followup_service import update_followup_on_edit


def mark_followup_visited(db: Session, followup_id: str, organization_id: str):
  
    followup = (
        db.query(FollowUp)
        .filter(FollowUp.id == followup_id, FollowUp.organization_id == organization_id)
        .first()
    )
    if not followup:
        return None

    followup.status = FollowupStatus.COMPLETED.value
    followup.visited_status = FollowupVisitStatus.VISIT.value
    followup.contacted_at = datetime.now()

    if followup.appointment_id:
        appointment = db.query(Appointment).filter(Appointment.id == followup.appointment_id).first()
        if appointment:
            appointment.status = AppointmentStatus.COMPLETED.value

    db.commit()
    db.refresh(followup)
    return followup


def mark_followup_contacted(db: Session, followup_id: str, organization_id: str):
   
    followup = (
        db.query(FollowUp)
        .filter(FollowUp.id == followup_id, FollowUp.organization_id == organization_id)
        .first()
    )
    if not followup:
        return None

    followup.status = FollowupStatus.COMPLETED.value
    followup.visited_status = FollowupVisitStatus.CONTACTED.value
    followup.contacted_at = datetime.now()

    if followup.appointment_id:
        appointment = db.query(Appointment).filter(Appointment.id == followup.appointment_id).first()
        if appointment:
            appointment.status = AppointmentStatus.COMPLETED.value

    db.commit()
    db.refresh(followup)
    return followup


def mark_followup_cancelled(db: Session, followup_id: str, organization_id: str):

    followup = (
        db.query(FollowUp)
        .filter(FollowUp.id == followup_id, FollowUp.organization_id == organization_id)
        .first()
    )
    if not followup:
        return None

    followup.status = FollowupStatus.CANCELLED.value
    followup.visited_status = FollowupVisitStatus.CANCELLED.value

    if followup.appointment_id:
        appointment = db.query(Appointment).filter(Appointment.id == followup.appointment_id).first()
        if appointment:
            appointment.status = AppointmentStatus.CANCELLED.value

    db.commit()
    db.refresh(followup)
    return followup


def reschedule_followup(
    db: Session,
    followup_id: str,
    organization_id: str,
    new_date: date,
    new_time: Optional[time] = None,
    new_duration: Optional[int] = None,
) -> Optional[FollowUp]:

    followup = (
        db.query(FollowUp)
        .filter(FollowUp.id == followup_id, FollowUp.organization_id == organization_id)
        .first()
    )
    if not followup:
        return None

    updated_followup = update_followup_on_edit(
        db=db,
        followup=followup,
        new_date=new_date,
        new_time=new_time,
        new_duration=new_duration,
    )

    db.commit()
    db.refresh(updated_followup)
    return updated_followup
