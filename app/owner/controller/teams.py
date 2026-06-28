from sqlalchemy.orm import Session
from app.model.User import User
from app.model.Roles import Roles as Role
from app.db.schemas.user import UserCreate, UserUpdate
from app.utils.auth_utils import hash_password
from app.utils.ApiResponse import success_response, not_found_response, error_response


def create_user(db: Session, user: UserCreate, organization_id: str):
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        password=hashed_password,
        name=user.name,
        role=user.role,
        phone=user.phone,
        specialization=user.specialization,
        description=user.description,
        profile_photo=user.profile_photo,
        status=user.status,
        organization_id=organization_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: str) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users_by_organization(db: Session, organization_id: str, skip: int = 0, limit: int = 10):
    return (
        db.query(User)
        .filter(User.organization_id == organization_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_user(db: Session, user_id: str, user_update: UserUpdate) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found", data="")

    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found", data="")
    db.delete(db_user)
    db.commit()
    return success_response("User deleted successfully", data="")


def assign_role_to_user(db: Session, user_id: str, role_id: str):
    """Fetch both user and role then add role to user.roles if not already assigned."""
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found", data="")
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return not_found_response("Role not found", data="")
    if db_role not in db_user.roles:
        db_user.roles.append(db_role)
        db.commit()
        db.refresh(db_user)
    return db_user


def remove_role_from_user(db: Session, user_id: str, role_id: str):
    """Fetch both user and role then remove role from user.roles."""
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found", data="")
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return not_found_response("Role not found", data="")
    if db_role in db_user.roles:
        db_user.roles.remove(db_role)
        db.commit()
        db.refresh(db_user)
    return db_user