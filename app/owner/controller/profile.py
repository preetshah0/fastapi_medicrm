from sqlalchemy.orm import Session
from app.model.User import User
from app.model.Organization import Organization
from app.db.schemas.profile import (
    ProfileUpdateRequest,
    OrganizationProfileUpdateRequest,
)
from app.utils.auth_utils import verify_password, hash_password


def get_user_profile(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def update_user_profile(
    db: Session, user: User, payload: ProfileUpdateRequest
) -> User:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def change_user_password(
    db: Session, user: User, current_password: str, new_password: str
) -> bool:
    if not verify_password(current_password, user.password):
        return False

    user.password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return True


def update_user_profile_photo(db: Session, user: User, photo_path: str) -> User:
    user.profile_photo = photo_path
    db.commit()
    db.refresh(user)
    return user


def get_organization_profile(
    db: Session, organization_id: str
) -> Organization | None:
    return (
        db.query(Organization)
        .filter(Organization.id == organization_id)
        .first()
    )


def update_organization_profile(
    db: Session, org: Organization, payload: OrganizationProfileUpdateRequest
) -> Organization:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(org, field):
            setattr(org, field, value)

    db.commit()
    db.refresh(org)
    return org

