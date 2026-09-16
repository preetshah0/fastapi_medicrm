from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.plan import PlanCreate, PlanUpdate, PlanResponse
from app.Enum.PlanStatus import PlanStatus
from app.model.Plan import Plan
from app.model.Subscription import Subscription
from app.admin.controller.plan import (
    get_plan_modules,
    get_slug,
    create_plan,
    get_plan,
    get_plans,
    update_plan,
    toggle_plan_status,
    delete_plan,
)
from app.utils.ApiResponse import (
    success_response,
    not_found_response,
    error_response,
    validation_error_response,
)

router = APIRouter(prefix="/admin/plans", tags=["plans"])


@router.get("/modules", response_model=APIResponse[list[dict]])
def get_plan_modules_route():
    """Fetch structured template list of all system modules for plan creation UI."""
    modules = get_plan_modules()
    return success_response("Plan modules fetched successfully", modules)


@router.post("/add", response_model=APIResponse[PlanResponse])
def create_plan_route(
    payload: PlanCreate,
    db: Session = Depends(get_db),
):
    
    slug = get_slug(payload.name)
    existing_plan = db.query(Plan).filter(Plan.slug == slug).first()
    if existing_plan:
        error_response(f"A plan with the name '{payload.name}' already exists.", data="")

   
    if payload.monthly_price < 0 or payload.yearly_price < 0:
        validation_error_response("Monthly and yearly prices cannot be negative values.", data="")

    if not payload.modules or not isinstance(payload.modules, dict):
        validation_error_response("Plan modules configuration is required.", data="")

   
    limits = {
        "max_appointments": payload.max_appointments,
        "max_patients": payload.max_patients,
        "max_staff": payload.max_staff,
        "max_lab_referrals": payload.max_lab_referrals,
    }
    for limit_key, limit_val in limits.items():
        if limit_val is not None and limit_val < -1:
            validation_error_response(
                f"Invalid limit value for '{limit_key}'. Limit must be -1 (unlimited) or a positive integer.",
                data="",
            )

    result = create_plan(db=db, plan=payload)
    return success_response("Plan created successfully", result)


@router.get("", response_model=APIResponse[List[PlanResponse]])
def get_plans_route(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """List all plans with optional status filtering."""
    if status and status not in [s.value for s in PlanStatus]:
        validation_error_response(
            f"Invalid status filter. Allowed values: {[s.value for s in PlanStatus]}", data=""
        )

    result = get_plans(db=db, status=status, skip=skip, limit=limit)
    return success_response("Plans fetched successfully", result)


@router.get("/{plan_id}", response_model=APIResponse[PlanResponse])
def get_plan_route(
    plan_id: str,
    db: Session = Depends(get_db),
):
    """Fetch plan details by plan ID."""
    result = get_plan(db=db, plan_id=plan_id)
    if not result:
        not_found_response("Plan not found.", data="")

    return success_response("Plan fetched successfully", result)


@router.put("/{plan_id}", response_model=APIResponse[PlanResponse])
def update_plan_route(
    plan_id: str,
    payload: PlanUpdate,
    db: Session = Depends(get_db),
):
    """Update existing plan parameters and modules."""
    db_plan = get_plan(db=db, plan_id=plan_id)
    if not db_plan:
        not_found_response("Plan not found.", data="")

    # Check for duplicate name/slug if name is modified
    if payload.name:
        new_slug = get_slug(payload.name)
        existing = db.query(Plan).filter(Plan.slug == new_slug, Plan.id != plan_id).first()
        if existing:
            error_response(f"Another plan with the name '{payload.name}' already exists.", data="")

    # Price validations
    if payload.monthly_price is not None and payload.monthly_price < 0:
        validation_error_response("Monthly price cannot be negative.", data="")
    if payload.yearly_price is not None and payload.yearly_price < 0:
        validation_error_response("Yearly price cannot be negative.", data="")

    # Limit validations
    limits = {
        "max_appointments": payload.max_appointments,
        "max_patients": payload.max_patients,
        "max_staff": payload.max_staff,
        "max_lab_referrals": payload.max_lab_referrals,
    }
    for limit_key, limit_val in limits.items():
        if limit_val is not None and limit_val < -1:
            validation_error_response(
                f"Invalid limit value for '{limit_key}'. Limit must be -1 (unlimited) or a positive integer.",
                data="",
            )

    result = update_plan(db=db, plan_id=plan_id, plan=payload)
    return success_response("Plan updated successfully", result)


@router.patch("/{plan_id}/toggle-status", response_model=APIResponse[PlanResponse])
def toggle_plan_status_route(
    plan_id: str,
    db: Session = Depends(get_db),
):
    """Toggle plan status between ACTIVE and INACTIVE."""
    db_plan = get_plan(db=db, plan_id=plan_id)
    if not db_plan:
        not_found_response("Plan not found.", data="")

    if db_plan.status == PlanStatus.DRAFT.value:
        error_response("Draft plans must be published before status can be toggled.", data="")

    result = toggle_plan_status(db=db, db_plan=db_plan)
    return success_response(f"Plan status updated to '{result.status}'", result)


@router.delete("/{plan_id}")
def delete_plan_route(
    plan_id: str,
    db: Session = Depends(get_db),
):
    """Delete a plan if it is not linked to active subscriptions."""
    db_plan = get_plan(db=db, plan_id=plan_id)
    if not db_plan:
        not_found_response("Plan not found.", data="")

    # Prevent deletion if active subscriptions exist for this plan
    active_subscription = (
        db.query(Subscription)
        .filter(Subscription.plan_id == plan_id)
        .first()
    )
    if active_subscription:
        error_response(
            "Cannot delete plan as it is linked to organization subscriptions.", data=""
        )

    delete_plan(db=db, plan_id=plan_id)
    return success_response("Plan deleted successfully", data="")
