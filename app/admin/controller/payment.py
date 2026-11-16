from typing import Optional, List, Dict, Any
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.model.Payment import Payment
from app.model.Organization import Organization
from app.Enum.PaymentStatus import PaymentStatus


def get_admin_payments(
    db: Session,
    status: Optional[str] = None,
    organization_id: Optional[str] = None,
    provider: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    query = (
        db.query(Payment)
        .join(Organization, Payment.organization_id == Organization.id)
    )

    if status:
        query = query.filter(Payment.status == status)

    if organization_id:
        query = query.filter(Payment.organization_id == organization_id)

    if provider:
        query = query.filter(Payment.provider == provider)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Payment.reference_no.ilike(term),
                Payment.provider_payment_id.ilike(term),
                Payment.provider_invoice_id.ilike(term),
                Organization.organization_name.ilike(term),
                Organization.ref.ilike(term),
            )
        )

    payments = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for p in payments:
        result.append({
            "id": p.id,
            "organization_id": p.organization_id,
            "organization_name": p.organization.organization_name if p.organization else None,
            "organization_ref": p.organization.ref if p.organization else None,
            "subscription_id": p.subscription_id,
            "amount": p.amount,
            "currency": p.currency,
            "payment_mode": p.payment_mode,
            "provider": p.provider,
            "provider_payment_id": p.provider_payment_id,
            "provider_invoice_id": p.provider_invoice_id,
            "paid_at": p.paid_at,
            "status": p.status,
            "reference_no": p.reference_no,
            "notes": p.notes,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
        })

    return result


def get_admin_payments_summary(db: Session) -> Dict[str, Any]:
    total_rev = (
        db.query(func.coalesce(func.sum(Payment.amount), Decimal("0.00")))
        .filter(Payment.status == PaymentStatus.PAID.value)
        .scalar()
    ) or Decimal("0.00")

    total_count = db.query(Payment).count()
    paid_count = db.query(Payment).filter(Payment.status == PaymentStatus.PAID.value).count()
    failed_count = db.query(Payment).filter(Payment.status == PaymentStatus.FAILED.value).count()
    pending_count = db.query(Payment).filter(Payment.status == PaymentStatus.PENDING.value).count()

    return {
        "total_revenue": total_rev,
        "currency": "USD",
        "total_count": total_count,
        "paid_count": paid_count,
        "failed_count": failed_count,
        "pending_count": pending_count,
    }

