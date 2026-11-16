from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.profile import (
    ProfileResponse,
    ProfileUpdateRequest,
    ChangePasswordRequest,
    OrganizationProfileResponse,
    OrganizationProfileUpdateRequest,
)
from app.model.User import User
from app.Enum.UserRole import UserRole
from app.owner.controller.profile import (
    update_user_profile,
    change_user_password,
    get_organization_profile,
    update_organization_profile,
)
from app.utils.auth_utils import get_current_user
from app.utils.ApiResponse import (
    success_response,
    not_found_response,
    error_response,
    unauthorized_response,
)

router = APIRouter(prefix="/owner/profile", tags=["owner-profile"])


@router.get("", response_model=APIResponse[ProfileResponse])
def get_profile(
    current_user: User = Depends(get_current_user),
):
    """Fetch current logged-in user profile."""
    return success_response("Profile fetched successfully", current_user)


@router.put("", response_model=APIResponse[ProfileResponse])
def update_profile(
    payload: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current logged-in user profile details."""
    updated_user = update_user_profile(db=db, user=current_user, payload=payload)
    return success_response("Profile updated successfully", updated_user)


@router.put("/change-password", response_model=APIResponse[dict])
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change current logged-in user password."""
    if not change_user_password(
        db=db,
        user=current_user,
        current_password=payload.current_password,
        new_password=payload.new_password,
    ):
        error_response("Current password is incorrect")

    return success_response("Password changed successfully", {})


@router.get("/organization", response_model=APIResponse[OrganizationProfileResponse])
def get_organization(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Fetch organization profile details for the logged-in user's organization."""
    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization")

    org = get_organization_profile(db=db, organization_id=current_user.organization_id)
    if not org:
        not_found_response("Organization not found")

    return success_response("Organization profile fetched successfully", org)


@router.put("/organization", response_model=APIResponse[OrganizationProfileResponse])
def update_organization(
    payload: OrganizationProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update organization profile details (Owner role only)."""
    if current_user.role != UserRole.OWNER.value:
        error_response("Only organization owners are permitted to update organization details")

    if not current_user.organization_id:
        unauthorized_response("User is not associated with any organization")

    org = get_organization_profile(db=db, organization_id=current_user.organization_id)
    if not org:
        not_found_response("Organization not found")

    updated_org = update_organization_profile(db=db, org=org, payload=payload)
    return success_response("Organization profile updated successfully", updated_org)
