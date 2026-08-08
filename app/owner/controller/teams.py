from sqlalchemy.orm import Session
from app.model.User import User
from app.model.Role import Roles as Role
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
        status=user.status.value,
        organization_id=organization_id
    )
    
    db_role = db.query(Role).filter(Role.name == user.role).first()
    if db_role:
        db_user.roles.append(db_role)

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


def update_user(db: Session, db_user: User, user_update: UserUpdate) -> User:
    update_data = user_update.model_dump(exclude_unset=True, mode='json')
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return True


def assign_role_to_user(db: Session, user: User, role: Role):
    if role not in user.roles:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
    return user


def remove_role_from_user(db: Session, user: User, role: Role):
    if role in user.roles:
        user.roles.remove(role)
        db.commit()
        db.refresh(user)
    return user