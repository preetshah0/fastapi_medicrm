import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.model.Payment import Payment


def generate_payment_reference(year: int | None = None) -> str:
    """Generate reference for payment transaction e.g., PAY-2026-00001"""
    curr_year = year or datetime.now().year
    suffix = uuid.uuid4().hex[:6].upper()
    return f"PAY-{curr_year}-{suffix}"


def get_organization_payments(
    db: Session,
    organization_id: str,
    skip: int = 0,
    limit: int = 50,
):
    """Retrieve billing payments history for the organization."""
    return (
        db.query(Payment)
        .filter(Payment.organization_id == organization_id)
        .order_by(Payment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

