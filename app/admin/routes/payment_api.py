from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.payment import AdminPaymentResponse, AdminPaymentSummaryResponse
from app.Enum.PaymentStatus import PaymentStatus
from app.Enum.PaymentProvider import PaymentProvider
from app.admin.controller.payment import (
    get_admin_payments,
    get_admin_payments_summary,
)
from app.utils.ApiResponse import success_response

router = APIRouter(prefix="/admin/payments", tags=["admin-payments"])


@router.get("/summary", response_model=APIResponse[AdminPaymentSummaryResponse])
def get_payments_summary(
    db: Session = Depends(get_db),
):
    """
    Fetch platform-wide revenue and transaction status summary.
    """
    summary = get_admin_payments_summary(db=db)
    return success_response("Payments summary fetched successfully", summary)


@router.get("", response_model=APIResponse[List[AdminPaymentResponse]])
def list_payments(
    status: Optional[PaymentStatus] = Query(default=None),
    organization_id: Optional[str] = Query(default=None),
    provider: Optional[PaymentProvider] = Query(default=None),
    search: Optional[str] = Query(default=None, description="Search by reference no, payment id, invoice id, or org name"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    payments = get_admin_payments(
        db=db,
        status=status.value if status else None,
        organization_id=organization_id,
        provider=provider.value if provider else None,
        search=search,
        skip=skip,
        limit=limit,
    )
    return success_response("Payments fetched successfully", payments)

