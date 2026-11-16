from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.model.Subscription import Subscription
from app.model.Organization import Organization
from app.model.Plan import Plan


def get_admin_subscriptions(
    db: Session,
    status: Optional[str] = None,
    plan_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    query = (
        db.query(Subscription)
        .join(Organization, Subscription.organization_id == Organization.id)
        .join(Plan, Subscription.plan_id == Plan.id)
    )

    if status:
        query = query.filter(Subscription.status == status)

    if plan_id:
        query = query.filter(Subscription.plan_id == plan_id)

    if organization_id:
        query = query.filter(Subscription.organization_id == organization_id)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Subscription.subscription_reference.ilike(term),
                Organization.organization_name.ilike(term),
                Organization.ref.ilike(term),
                Plan.name.ilike(term),
            )
        )

    subs = query.order_by(Subscription.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for sub in subs:
        result.append({
            "id": sub.id,
            "subscription_reference": sub.subscription_reference,
            "organization_id": sub.organization_id,
            "organization_name": sub.organization.organization_name if sub.organization else None,
            "organization_ref": sub.organization.ref if sub.organization else None,
            "plan_id": sub.plan_id,
            "plan_name": sub.plan.name if sub.plan else None,
            "start_date": sub.start_date,
            "end_date": sub.end_date,
            "total_billing_amount": sub.total_billing_amount,
            "currency": sub.currency,
            "billing_period": sub.billing_period,
            "auto_renew": sub.auto_renew,
            "cancelled_at": sub.cancelled_at,
            "status": sub.status,
            "stripe_subscription_id": sub.stripe_subscription_id,
            "stripe_checkout_session_id": sub.stripe_checkout_session_id,
            "created_at": sub.created_at,
            "updated_at": sub.updated_at,
        })

    return result


def get_admin_subscription_by_id(db: Session, subscription_id: str) -> Optional[Dict[str, Any]]:
    sub = (
        db.query(Subscription)
        .filter(Subscription.id == subscription_id)
        .first()
    )
    if not sub:
        return None

    return {
        "id": sub.id,
        "subscription_reference": sub.subscription_reference,
        "organization_id": sub.organization_id,
        "organization_name": sub.organization.organization_name if sub.organization else None,
        "organization_ref": sub.organization.ref if sub.organization else None,
        "plan_id": sub.plan_id,
        "plan_name": sub.plan.name if sub.plan else None,
        "start_date": sub.start_date,
        "end_date": sub.end_date,
        "total_billing_amount": sub.total_billing_amount,
        "currency": sub.currency,
        "billing_period": sub.billing_period,
        "auto_renew": sub.auto_renew,
        "cancelled_at": sub.cancelled_at,
        "status": sub.status,
        "stripe_subscription_id": sub.stripe_subscription_id,
        "stripe_checkout_session_id": sub.stripe_checkout_session_id,
        "created_at": sub.created_at,
        "updated_at": sub.updated_at,
    }

