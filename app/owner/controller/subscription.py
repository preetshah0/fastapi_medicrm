from app.owner.controller.payment import generate_payment_reference
from app.admin.controller.plan import get_plan
from app.model import User, Organization, Plan, Subscription, Payment
from app.db.schemas.stripe import (
    StripeCustomerCreate,
    StripeCheckoutRequest,
    StripeCheckoutSessionCreate,
    StripePortalCreate,
)
from app.services.stripe_gateway import (
    create_customer,
    get_customer,
    create_checkout_session,
    expire_checkout_session,
    cancel_subscription as gateway_cancel_subscription,
    set_subscription_cancel_at_period_end,
    create_billing_portal_session,
)
from app.Enum.BillingPeriod import BillingPeriod
from app.Enum.SubscriptionStatus import SubscriptionStatus
from app.Enum.AutoRenew import AutoRenew
from app.Enum.PaymentStatus import PaymentStatus
from app.core.config import settings
from app.utils.ApiResponse import error_response, not_found_response
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import time
import re
def generate_subscription_reference(db: Session, year: int | None = None) -> str:

    current_year = year if year is not None else datetime.now().year
    prefix = f"SUB-{current_year:04d}"

    latest_ref = (
        db.query(Subscription.subscription_reference)
        .filter(Subscription.subscription_reference.like(f"{prefix}-%"))
        .order_by(
            func.length(Subscription.subscription_reference).desc(),
            Subscription.subscription_reference.desc(),
        )
        .first()
    )

    max_seq = 0
    if latest_ref and latest_ref[0]:
        match = re.search(r"-(\d+)$", str(latest_ref[0]))
        if match:
            max_seq = int(match.group(1))

    next_seq = max_seq + 1
    while True:
        ref = f"{prefix}-{next_seq:05d}"
        exists = (
            db.query(Subscription.id)
            .filter(Subscription.subscription_reference == ref)
            .first()
        )
        if not exists:
            return ref
        next_seq += 1


def validate_plan(db: Session, plan_id: str, billing_period: BillingPeriod):
    """
    Fast, local validation: retrieves the plan and its matching Stripe price ID.
    """
    plan = get_plan(db=db, plan_id=plan_id)
    if not plan or not plan.status:
        return False
    if billing_period == BillingPeriod.MONTHLY:
        price_id = plan.stripe_monthly_price_id
    elif billing_period == BillingPeriod.YEARLY:
        price_id = plan.stripe_yearly_price_id
    else:
        return False
    if not price_id:
        return False
    return price_id, plan

def ensure_customer(db: Session, organization:Organization, owner: User):
    customer = get_customer(organization.stripe_customer_id)
    if not customer:
            customer_email = organization.organization_email or owner.email
            payload = StripeCustomerCreate(
                name=organization.organization_name,
                email=customer_email,
                metadata={"organization_id": str(organization.id), "owner_id": str(owner.id)},
            )
            customer = create_customer(payload)
            organization.stripe_customer_id = customer.id
            db.commit()
            db.refresh(organization)
            return customer.id
    return organization.stripe_customer_id
        

def checkout_session(db:Session, organization_id: str, payload: StripeCheckoutRequest, current_user_id: str):
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        return False
    owner = db.query(User).filter(User.id == current_user_id).first()
    if not owner:
        return False

    plan_check = validate_plan(
        db=db,
        plan_id=payload.plan_id,
        billing_period=payload.billing_period,
    )
    if not plan_check:
        return False

    price_id, plan = plan_check

    customer = ensure_customer(db, organization, owner)
    if not customer:
        return False

    # Check if organization already has an unexpired subscription for this exact plan
    existing_plan_sub = (
        db.query(Subscription)
        .filter(
            Subscription.organization_id == organization.id,
            Subscription.plan_id == plan.id,
            Subscription.status.in_([SubscriptionStatus.ACTIVE.value, SubscriptionStatus.INACTIVE.value]),
        )
        .first()
    )
    if existing_plan_sub:
        if not existing_plan_sub.end_date or existing_plan_sub.end_date > datetime.now():
            return False

    amount = (
        plan.monthly_price
        if payload.billing_period == BillingPeriod.MONTHLY
        else plan.yearly_price
    )

    # URLs directly to frontend with Stripe's dynamic {CHECKOUT_SESSION_ID}
    frontend_base = settings.FRONT_END_URL.rstrip("/")
    success_url = f"{frontend_base}/checkout/thank-you?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{frontend_base}/checkout/cancel"

    metadata = {
        "organization_id": str(organization.id),
        "owner_id": str(owner.id),
        "plan_id": str(plan.id),
        "billing_period": payload.billing_period.value,
    }

    try:
        session = create_checkout_session(
            StripeCheckoutSessionCreate(
                customer_id=customer,
                price_id=price_id,
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata,
            )
        )
    except Exception:
        return False

    return {
        "checkout_url": session.url,
        "session_id": session.id,
    }


def cancel_active_subscription(db: Session, organization_id: str):

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.organization_id == organization_id,
            Subscription.status == SubscriptionStatus.ACTIVE.value,
        )
        .first()
    )
    if not subscription:
        return False

    if subscription.stripe_subscription_id:
        try:
            from app.db.schemas.stripe import StripeCancelSubscriptionRequest
            gateway_cancel_subscription(
                StripeCancelSubscriptionRequest(
                    subscription_id=subscription.stripe_subscription_id,
                    at_period_end=False,
                )
            )
        except Exception:
            return False

    subscription.status = SubscriptionStatus.CANCELLED.value
    subscription.auto_renew = AutoRenew.INACTIVE.value
    subscription.cancelled_at = datetime.now()
    subscription.end_date = datetime.now()

    db.commit()
    db.refresh(subscription)
    return subscription


def create_customer_portal_session(db: Session, organization_id: str, return_url: str | None = None):
    """
    Generate a Stripe Customer Portal link for the organization owner.
    Enables self-serve credit card updating, payment method changes, and invoice downloading.
    """
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org or not org.stripe_customer_id:
        return False

    frontend_return = return_url or f"{settings.FRONT_END_URL.rstrip('/')}/subscription"

    try:
        portal = create_billing_portal_session(
            StripePortalCreate(
                customer_id=org.stripe_customer_id,
                return_url=frontend_return,
            )
        )
        return {"portal_url": portal.url}
    except Exception:
        return False


def toggle_subscription_auto_renew(db: Session, organization_id: str):
    """
    Toggle auto-renew for the organization's active subscription.
    If active -> marks inactive and sets cancel_at_period_end=True in Stripe.
    If inactive -> marks active and sets cancel_at_period_end=False in Stripe.
    """
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.organization_id == organization_id,
            Subscription.status == SubscriptionStatus.ACTIVE.value,
        )
        .first()
    )
    if not subscription or not subscription.stripe_subscription_id:
        return False

    is_currently_active = subscription.auto_renew == AutoRenew.ACTIVE.value
    new_cancel_at_period_end = is_currently_active  # True if we want to turn it OFF

    try:
        set_subscription_cancel_at_period_end(
            subscription.stripe_subscription_id,
            cancel_at_period_end=new_cancel_at_period_end,
        )
    except Exception:
        return False

    subscription.auto_renew = (
        AutoRenew.INACTIVE.value if is_currently_active else AutoRenew.ACTIVE.value
    )
    db.commit()
    db.refresh(subscription)
    return subscription


def switch_active_subscription(db: Session, organization_id: str, target_subscription_id: str):
    """
    Switch active subscription to another purchased, unexpired subscription.
    Enforces that only one subscription is ACTIVE at any time; the previous becomes INACTIVE.
    Once upgraded, user cannot switch back to a free plan unless all paid plans are expired.
    """
    target_sub = (
        db.query(Subscription)
        .filter(
            Subscription.id == target_subscription_id,
            Subscription.organization_id == organization_id,
        )
        .first()
    )
    if not target_sub:
        return False

    if target_sub.status == SubscriptionStatus.ACTIVE.value:
        return False

    if target_sub.status == SubscriptionStatus.CANCELLED.value:
        return False

    target_price = (
        target_sub.plan.monthly_price
        if target_sub.billing_period == BillingPeriod.MONTHLY.value
        else target_sub.plan.yearly_price
    ) if target_sub.plan else target_sub.total_billing_amount

    is_target_free = (target_price == 0) or (target_sub.total_billing_amount == 0)

    # Free plans never expire; paid plans must not be expired
    if not is_target_free:
        if target_sub.status == SubscriptionStatus.EXPIRED.value:
            return False
        if target_sub.end_date and target_sub.end_date < datetime.now():
            return False

    # Free plan restriction: Cannot switch to free if any paid plan is bought and neither expired nor cancelled
    if is_target_free:
        has_valid_paid_sub = (
            db.query(Subscription)
            .filter(
                Subscription.organization_id == organization_id,
                Subscription.id != target_sub.id,
                Subscription.status.in_([SubscriptionStatus.ACTIVE.value, SubscriptionStatus.INACTIVE.value]),
                Subscription.total_billing_amount > 0,
                Subscription.cancelled_at.is_(None),
                (Subscription.end_date.is_(None) | (Subscription.end_date > datetime.now())),
            )
            .first()
        )
        if has_valid_paid_sub:
            return False

    # Deactivate current active subscription(s)
    db.query(Subscription).filter(
        Subscription.organization_id == organization_id,
        Subscription.status == SubscriptionStatus.ACTIVE.value,
    ).update({"status": SubscriptionStatus.INACTIVE.value}, synchronize_session=False)

    # Activate target subscription
    target_sub.status = SubscriptionStatus.ACTIVE.value
    db.commit()
    db.refresh(target_sub)
    return target_sub


def get_organization_subscriptions(db: Session, organization_id: str):

    return (
        db.query(Subscription)
        .filter(Subscription.organization_id == organization_id)
        .order_by(Subscription.created_at.desc())
        .all()
    )