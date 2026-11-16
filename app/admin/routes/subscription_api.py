from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.subscription import AdminSubscriptionResponse
from app.Enum.SubscriptionStatus import SubscriptionStatus
from app.admin.controller.subscription import (
    get_admin_subscriptions,
    get_admin_subscription_by_id,
)
from app.utils.ApiResponse import success_response, not_found_response

router = APIRouter(prefix="/admin/subscriptions", tags=["admin-subscriptions"])


@router.get("", response_model=APIResponse[List[AdminSubscriptionResponse]])
def list_subscriptions(
    status: Optional[SubscriptionStatus] = Query(default=None),
    plan_id: Optional[str] = Query(default=None),
    organization_id: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None, description="Search by subscription reference, org name, or plan name"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    List all organization subscriptions across the platform with filtering and search.
    """
    subs = get_admin_subscriptions(
        db=db,
        status=status.value if status else None,
        plan_id=plan_id,
        organization_id=organization_id,
        search=search,
        skip=skip,
        limit=limit,
    )
    return success_response("Subscriptions fetched successfully", subs)


@router.get("/{subscription_id}", response_model=APIResponse[AdminSubscriptionResponse])
def get_subscription_details(
    subscription_id: str,
    db: Session = Depends(get_db),
):
    """
    Fetch single subscription details by ID with organization and plan info.
    """
    sub = get_admin_subscription_by_id(db=db, subscription_id=subscription_id)
    if not sub:
        not_found_response("Subscription not found")

    return success_response("Subscription fetched successfully", sub)

