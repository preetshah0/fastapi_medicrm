from typing import Optional
from datetime import date, time
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.followups import FollowUpResponse, RescheduleFollowupRequest
from app.owner.controller.followup import (
    mark_followup_visited,
    mark_followup_contacted,
    mark_followup_cancelled,
    reschedule_followup,
)
from app.utils.ApiResponse import success_response, not_found_response
from app.utils.auth_utils import require_permission

router = APIRouter(prefix="/owner/followups", tags=["followups"])


@router.patch(
    "/{followup_id}/visited/organization/{organization_id}",
    dependencies=[Depends(require_permission("follow-ups", action="edit"))],
    response_model=APIResponse[FollowUpResponse],
)
def mark_visited_route(
    followup_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    result = mark_followup_visited(db=db, followup_id=followup_id, organization_id=organization_id)
    if not result:
        return not_found_response("Follow-up not found", data="")
    return success_response("Follow-up marked as visited successfully", result)


@router.patch(
    "/{followup_id}/contacted/organization/{organization_id}",
    dependencies=[Depends(require_permission("follow-ups", action="edit"))],
    response_model=APIResponse[FollowUpResponse],
)
def mark_contacted_route(
    followup_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    result = mark_followup_contacted(db=db, followup_id=followup_id, organization_id=organization_id)
    if not result:
        return not_found_response("Follow-up not found", data="")
    return success_response("Follow-up marked as contacted successfully", result)


@router.patch(
    "/{followup_id}/cancelled/organization/{organization_id}",
    dependencies=[Depends(require_permission("follow-ups", action="edit"))],
    response_model=APIResponse[FollowUpResponse],
)
def mark_cancelled_route(
    followup_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    result = mark_followup_cancelled(db=db, followup_id=followup_id, organization_id=organization_id)
    if not result:
        return not_found_response("Follow-up not found", data="")
    return success_response("Follow-up marked as cancelled successfully", result)


@router.put(
    "/{followup_id}/reschedule/organization/{organization_id}",
    dependencies=[Depends(require_permission("follow-ups", action="edit"))],
    response_model=APIResponse[FollowUpResponse],
)
def reschedule_followup_route(
    followup_id: str,
    organization_id: str,
    payload: RescheduleFollowupRequest,
    db: Session = Depends(get_db)
):
    result = reschedule_followup(
        db=db,
        followup_id=followup_id,
        organization_id=organization_id,
        new_date=payload.new_date,
        new_time=payload.new_time,
        new_duration=payload.new_duration
    )
    if not result:
        return not_found_response("Follow-up not found", data="")
    return success_response("Follow-up rescheduled successfully", result)

