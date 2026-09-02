from sqlalchemy.orm import Session
from app.model.Role import Roles as Role, Permissions
from app.db.schemas.role import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate, PermissionResponse
from app.utils.ApiResponse import success_response, error_response, not_found_response

import random

def generate_slug(title: str) -> str:
    return title.lower().replace(" ", "-")

def create_role(db: Session, role: RoleCreate) -> Role:
    slug = role.slug if role.slug else generate_slug(role.name)
    db_role = Role(name=role.name, slug=slug)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_role(db: Session, role_id: str) -> Role:
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, role_name: str) -> Role:
    return db.query(Role).filter(Role.name == role_name).first()


def get_role_by_slug(db: Session, role_slug: str) -> Role:
    return db.query(Role).filter(Role.slug == role_slug).first()


def update_role(db: Session, role_slug: str, role_update: RoleUpdate) -> Role:
    db_role = get_role_by_slug(db, role_slug)
    # if not db_role:
    #     return error_response("Role not found", data="")

    update_data = role_update.dict(exclude_unset=True)
    if "name" in update_data and "slug" not in update_data:
        update_data["slug"] = generate_slug(update_data["name"])

    if "slug" in update_data:
        existing_item = db.query(Role).filter(Role.slug == update_data["slug"]).first()
        if existing_item and existing_item.id != db_role.id:
            return error_response("Role with this slug already exists", data="")

    for key, value in update_data.items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_slug: str) -> bool:
    db_role = get_role_by_slug(db, role_slug)
    if not db_role:
        return error_response("Role not found", data="")
    db.delete(db_role)
    db.commit()
    return success_response("Role deleted successfully", data="")


def get_all_roles(db: Session, skip: int = 0, limit: int = 100) -> list[Role]:
    return db.query(Role).offset(skip).limit(limit).all()


def get_permission(db: Session, permission_id: str) -> Permissions:
    return db.query(Permissions).filter(Permissions.id == permission_id).first()


def get_permission_by_slug(db: Session, permission_slug: str) -> Permissions:
    return db.query(Permissions).filter(Permissions.slug == permission_slug).first()


def create_permission(db: Session, permission: PermissionCreate) -> Permissions:
    slug = permission.slug if permission.slug else generate_slug(permission.permission)
    db_permission = Permissions(permission=permission.permission, slug=slug)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def update_permission(db: Session, permission_slug: str, permission_update: PermissionUpdate) -> Permissions:
    db_permission = get_permission_by_slug(db, permission_slug)
    if not db_permission:
        return error_response("Permission not found", data="")

    update_data = permission_update.dict(exclude_unset=True)
    if "permission" in update_data and "slug" not in update_data:
        update_data["slug"] = generate_slug(update_data["permission"])

    if "slug" in update_data:
        existing_item = db.query(Permissions).filter(Permissions.slug == update_data["slug"]).first()
        if existing_item and existing_item.id != db_permission.id:
            return error_response("Permission with this slug already exists", data="")

    for key, value in update_data.items():
        setattr(db_permission, key, value)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def delete_permission(db: Session, permission_slug: str) -> bool:
    db_permission = get_permission_by_slug(db, permission_slug)
    if not db_permission:
        return error_response("Permission not found", data="")
    db.delete(db_permission)
    db.commit()
    return success_response("Permission deleted successfully", data="")


def add_permission_to_role(db: Session, role: Role, permission: Permissions) -> Role:
    if permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()
        db.refresh(role)
    return role


def remove_permission_from_role(db: Session, role: Role, permission: Permissions) -> Role:
    if permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()
        db.refresh(role)
    return role
