from datetime import datetime, date, time, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.model.FollowUp import FollowUp, PrescriptionFollowUp, AppointmentFollowUp
from app.Enum.FollowupStatus import FollowupStatus
from app.Enum.FollowupVisitStatus import FollowupVisitStatus


def calculate_followup_end_time(followup_time: time, followup_duration: int) -> time:
    """
    Calculates and returns the follow-up end time by adding followup_duration (in minutes) to followup_time.
    """
    dummy_date = date.today()
    start_datetime = datetime.combine(dummy_date, followup_time)
    end_datetime = start_datetime + timedelta(minutes=followup_duration)
    return end_datetime.time()


def mark_overdue_followups(db: Session) -> int:
    """
    Checks follow-ups with status SCHEDULED or RESCHEDULED whose appointed end time has passed,
    and updates their status to OVERDUE.
    """
    now = datetime.now()
    today = now.date()
    current_time = now.time()

    followups = (
        db.query(FollowUp)
        .filter(FollowUp.status.in_([FollowupStatus.SCHEDULED.value, FollowupStatus.RESCHEDULED.value]))
        .all()
    )

    overdue_count = 0
    for followup in followups:
        if not followup.followup_date:
            continue

        end_time = (
            calculate_followup_end_time(followup.followup_time, followup.followup_duration)
            if (followup.followup_time is not None and followup.followup_duration is not None)
            else followup.followup_time
        )

        is_past_date = followup.followup_date < today
        is_same_date_past_time = (
            followup.followup_date == today
            and end_time is not None
            and end_time < current_time
        )

        if is_past_date or is_same_date_past_time:
            followup.status = FollowupStatus.OVERDUE.value
            overdue_count += 1

    if overdue_count > 0:
        db.commit()

    return overdue_count


def update_followup_on_edit(
    db: Session,
    followup: FollowUp,
    new_date: Optional[date] = None,
    new_time: Optional[time] = None,
    new_duration: Optional[int] = None,
    patient_id: Optional[str] = None,
    doctor_id: Optional[str] = None,
    branch_id: Optional[str] = None,
) -> FollowUp:
    """
    Updates follow-up details when prescription or appointment date/time is edited.
    If the existing follow-up status is OVERDUE, it leaves the existing entry untouched
    and creates a NEW follow-up entry with status RESCHEDULED.
    """
    if followup.status == FollowupStatus.OVERDUE.value:
        # Determine the target model class explicitly (PrescriptionFollowUp or AppointmentFollowUp)
        followup_cls = (
            PrescriptionFollowUp
            if followup.followable_type == "prescription"
            else AppointmentFollowUp
        )

        new_followup = followup_cls(
            organization_id=followup.organization_id,
            branch_id=branch_id if branch_id is not None else followup.branch_id,
            patient_id=patient_id if patient_id is not None else followup.patient_id,
            doctor_id=doctor_id if doctor_id is not None else followup.doctor_id,
            prescription_id=getattr(followup, "prescription_id", None),
            appointment_id=getattr(followup, "appointment_id", None),
            followable_type=followup.followable_type,
            followable_id=followup.followable_id,
            followup_date=new_date if new_date is not None else followup.followup_date,
            followup_time=new_time if new_time is not None else followup.followup_time,
            followup_duration=new_duration if new_duration is not None else followup.followup_duration,
            status=FollowupStatus.RESCHEDULED.value,
            visited_status=FollowupVisitStatus.PENDING.value,
        )
        db.add(new_followup)
        return new_followup
    else:
        if new_date is not None:
            followup.followup_date = new_date
        if new_time is not None:
            followup.followup_time = new_time
        if new_duration is not None:
            followup.followup_duration = new_duration
        if patient_id is not None:
            followup.patient_id = patient_id
        if doctor_id is not None:
            followup.doctor_id = doctor_id
        if branch_id is not None:
            followup.branch_id = branch_id

        return followup
