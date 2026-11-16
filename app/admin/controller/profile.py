from sqlalchemy.orm import Session
from app.model.User import User
from app.Enum.UserRole import UserRole
from app.db.schemas.profile import ProfileUpdateRequest
from app.utils.auth_utils import verify_password, hash_password


def get_admin_profile(db: Session, admin_id: str) -> User | None:
    return (
        db.query(User)
        .filter(User.id == admin_id, User.role == UserRole.ADMIN.value)
        .first()
    )


def update_admin_profile(
    db: Session, admin: User, payload: ProfileUpdateRequest
) -> User:
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(admin, field):
            setattr(admin, field, value)

    db.commit()
    db.refresh(admin)
    return admin


def change_admin_password(
    db: Session, admin: User, current_password: str, new_password: str
):
    if not verify_password(current_password, admin.password):
        return False

    admin.password = hash_password(new_password)
    db.commit()
    db.refresh(admin)
    return True


def update_admin_profile_photo(db: Session, admin: User, photo_path: str) -> User:
    admin.profile_photo = photo_path
    db.commit()
    db.refresh(admin)
    return admin

