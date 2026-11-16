from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.payment import PaymentResponse
from app.model.User import User
from app.auth.controller.user_auth import get_current_user
from app.owner.controller.payment import get_organization_payments
from app.utils.ApiResponse import success_response, unauthorized_response

router = APIRouter(prefix="/owner/payments", tags=["owner-payments"])


@router.get("/", response_model=APIResponse[list[PaymentResponse]])
def get_payments(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve billing payments and renewal receipts for the organization.
    """
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization.")

    payments = get_organization_payments(
        db=db,
        organization_id=current_user.organization_id,
        skip=skip,
        limit=limit,
    )
    return success_response("Payments retrieved successfully", payments)
