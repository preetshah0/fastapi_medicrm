from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.model.Role import Roles as Role
from app.db.schemas import UserCreate, UserUpdate, UserResponse, APIResponse
from app.owner.controller.teams import (
    create_user,
    get_user,
    get_users_by_organization,
    update_user,
    delete_user,
    assign_role_to_user,
    remove_role_from_user,
)
from app.utils.ApiResponse import success_response, not_found_response

router = APIRouter(prefix="/owner/teams", tags=["teams"])


@router.post("/add", response_model=APIResponse[UserResponse])
def add_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return success_response("User added successfully", create_user(db, user))


@router.get("/user/{user_id}", response_model=APIResponse[UserResponse])
def get_user_route(user_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found")
    return success_response("User fetched successfully", db_user)


@router.get("/organization/{organization_id}", response_model=APIResponse[list[UserResponse]])
def get_users_route(
    organization_id: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    return success_response(
        "Users fetched successfully",
        get_users_by_organization(db, organization_id, skip, limit),
    )


@router.put("/{user_id}", response_model=APIResponse[UserResponse])
def update_user_route(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found")
    return success_response("User updated successfully", update_user(db, db_user, user))


@router.delete("/{user_id}")
def delete_user_route(user_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found")
    delete_user(db, db_user)
    return success_response("User deleted successfully", data="")


@router.post("/{user_id}/role/{role_id}", response_model=APIResponse[UserResponse])
def assign_role_route(user_id: str, role_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found")
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return not_found_response("Role not found")
    return success_response("Role assigned successfully", assign_role_to_user(db, db_user, db_role))


@router.delete("/{user_id}/role/{role_id}", response_model=APIResponse[UserResponse])
def remove_role_route(user_id: str, role_id: str, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if not db_user:
        return not_found_response("User not found")
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return not_found_response("Role not found")
    return success_response("Role removed successfully", remove_role_from_user(db, db_user, db_role))
