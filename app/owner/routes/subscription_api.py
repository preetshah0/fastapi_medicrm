from typing import Optional
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.stripe import (
    StripeCheckoutRequest,
    StripeCheckoutResponse,
    StripePortalRequest,
    StripePortalResponse,
)
from app.db.schemas.subscription import SubscriptionResponse
from app.model.User import User
from app.model.Subscription import Subscription
from app.Enum.SubscriptionStatus import SubscriptionStatus
from app.Enum.AutoRenew import AutoRenew
from app.auth.controller.user_auth import get_current_user
from app.owner.controller.subscription import (
    checkout_session,
    cancel_active_subscription,
    switch_active_subscription,
    get_organization_subscriptions,
    toggle_subscription_auto_renew,
    create_customer_portal_session,
)
from app.utils.ApiResponse import success_response, error_response, not_found_response, unauthorized_response

router = APIRouter(prefix="/owner/subscription", tags=["owner-subscription"])


@router.post("/subscribe", response_model=APIResponse[StripeCheckoutResponse])
def subscribe(
    payload: StripeCheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Start subscription checkout session for the organization.
    Returns checkout_url to redirect user to Stripe.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    result = checkout_session(
        db=db,
        organization_id=current_user.organization_id,
        payload=payload,
        current_user_id=current_user.id,
    )

    if not result:
        error_response("Failed to initiate checkout session. Check plan or active subscription.")

    return success_response("Checkout session created successfully", result)


@router.get("/current", response_model=APIResponse[SubscriptionResponse])
def get_current_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve the organization's current active subscription details.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.organization_id == current_user.organization_id,
            Subscription.status == SubscriptionStatus.ACTIVE.value,
        )
        .first()
    )
    if not subscription:
        not_found_response("No active subscription found for your organization.")

    return success_response("Current subscription fetched successfully", subscription)


@router.post("/cancel", response_model=APIResponse[SubscriptionResponse])
def cancel_subscription_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel the organization's active subscription immediately.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    result = cancel_active_subscription(
        db=db,
        organization_id=current_user.organization_id,
    )

    if not result:
        error_response("No active subscription found to cancel or cancellation failed.")

    return success_response("Subscription cancelled immediately", result)


@router.post("/toggle-auto-renew", response_model=APIResponse[SubscriptionResponse])
def toggle_auto_renew_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Toggle recurring auto-renew for the active subscription.
    Turns auto-renewal ON or OFF without cancelling immediately.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    result = toggle_subscription_auto_renew(
        db=db,
        organization_id=current_user.organization_id,
    )
    if not result:
        error_response("Failed to toggle auto-renew. Check if you have an active paid subscription.")

    msg = (
        "Auto-renew enabled successfully"
        if result.auto_renew == AutoRenew.ACTIVE.value
        else "Auto-renew disabled successfully. Your plan will not renew at the end of billing period."
    )
    return success_response(msg, result)


@router.post("/portal", response_model=APIResponse[StripePortalResponse])
def customer_portal_route(
    payload: Optional[StripePortalRequest] = Body(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a Stripe Customer Portal link to update credit cards, payment methods, and view receipts.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    return_url = payload.return_url if payload else None
    result = create_customer_portal_session(
        db=db,
        organization_id=current_user.organization_id,
        return_url=return_url,
    )
    if not result:
        error_response("Failed to generate Customer Portal session. No customer account found.")

    return success_response("Customer portal session created successfully", result)


@router.get("/all", response_model=APIResponse[list[SubscriptionResponse]])
def get_all_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all subscriptions (active, inactive, expired, cancelled) for the organization.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    subscriptions = get_organization_subscriptions(
        db=db,
        organization_id=current_user.organization_id,
    )
    return success_response("Organization subscriptions fetched successfully", subscriptions)


@router.post("/switch/{subscription_id}", response_model=APIResponse[SubscriptionResponse])
def switch_subscription_route(
    subscription_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Switch the active plan to another purchased, unexpired subscription.
    Ensures that only one subscription is ACTIVE, while the previous one becomes INACTIVE.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    result = switch_active_subscription(
        db=db,
        organization_id=current_user.organization_id,
        target_subscription_id=subscription_id,
    )

    if not result:
        error_response("Failed to switch subscription. Target subscription may be invalid, expired, cancelled, or already active.")

    return success_response("Subscription switched successfully", result)
