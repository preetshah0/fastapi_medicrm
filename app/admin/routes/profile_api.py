from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.profile import (
    ProfileResponse,
    ProfileUpdateRequest,
    ChangePasswordRequest,
)
from app.model.User import User
from app.admin.controller.profile import (
    update_admin_profile,
    change_admin_password,
)
from app.utils.auth_utils import get_current_admin
from app.utils.ApiResponse import (
    success_response,
    error_response,
)

router = APIRouter(prefix="/admin/profile", tags=["admin-profile"])


@router.get("", response_model=APIResponse[ProfileResponse])
def get_profile(
    admin: User = Depends(get_current_admin),
):
    """Fetch current logged-in admin profile."""
    return success_response("Admin profile fetched successfully", admin)


@router.put("", response_model=APIResponse[ProfileResponse])
def update_profile(
    payload: ProfileUpdateRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Update current logged-in admin profile details."""
    updated_admin = update_admin_profile(db=db, admin=admin, payload=payload)
    return success_response("Admin profile updated successfully", updated_admin)


@router.put("/change-password", response_model=APIResponse[dict])
def change_password(
    payload: ChangePasswordRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Change current logged-in admin password."""
    if not change_admin_password(
        db=db,
        admin=admin,
        current_password=payload.current_password,
        new_password=payload.new_password,
    ):
        error_response("Current password is incorrect")

    return success_response("Password changed successfully", {})
