from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
    APIResponse,
)
from app.auth.controller.role import (
    create_role,
    get_role_by_slug,
    get_all_roles,
    update_role,
    delete_role,
    get_permission_by_slug,
    create_permission,
    update_permission,
    delete_permission,
    add_permission_to_role,
    remove_permission_from_role,
    generate_slug,
)
from app.utils.ApiResponse import success_response, not_found_response, error_response

router = APIRouter(prefix="/auth/roles", tags=["roles"])


# ── Role endpoints ──────────────────────────────────────────────────────────

@router.post("/create", response_model=APIResponse[RoleResponse])
def create_role_route(role: RoleCreate, db: Session = Depends(get_db)):
    existing_role = get_role_by_slug(db, role.name)
    if existing_role:
        return error_response("Role already exists")
    else:
        return success_response("Role created successfully", create_role(db, role))


@router.get("/all", response_model=APIResponse[list[RoleResponse]])
def get_all_roles_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return success_response("Roles fetched successfully", get_all_roles(db, skip, limit))


@router.get("/{role_slug}", response_model=APIResponse[RoleResponse])
def get_role_route(role_slug: str, db: Session = Depends(get_db)):
    db_role = get_role_by_slug(db, role_slug)
    if not db_role:
        return not_found_response("Role not found")
    return success_response("Role fetched successfully", db_role)


@router.put("/{role_slug}", response_model=APIResponse[RoleResponse])
def update_role_route(role_slug: str, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = get_role_by_slug(db, role_slug)
    if not db_role:
        return not_found_response("Role not found")
    else:
        return success_response("Role updated successfully", update_role(db, role_slug, role))


@router.delete("/{role_slug}")
def delete_role_route(role_slug: str, db: Session = Depends(get_db)):
    return delete_role(db, role_slug)


# ── Permission endpoints ────────────────────────────────────────────────────

@router.post("/permissions/create", response_model=APIResponse[PermissionResponse])
def create_permission_route(permission: PermissionCreate, db: Session = Depends(get_db)):
    slug = permission.slug if permission.slug else generate_slug(permission.permission)
    existing_permission = get_permission_by_slug(db, slug)
    if existing_permission:
        return error_response("Permission already exists")
    else:
        return success_response("Permission created successfully", create_permission(db, permission))


@router.get("/permissions/{permission_slug}", response_model=APIResponse[PermissionResponse])
def get_permission_route(permission_slug: str, db: Session = Depends(get_db)):
    db_perm = get_permission_by_slug(db, permission_slug)
    if not db_perm:
        return not_found_response("Permission not found")
    return success_response("Permission fetched successfully", db_perm)


@router.put("/permissions/{permission_slug}", response_model=APIResponse[PermissionResponse])
def update_permission_route(permission_slug: str, permission: PermissionUpdate, db: Session = Depends(get_db)):
    db_perm = get_permission_by_slug(db, permission_slug)
    if not db_perm:
        return not_found_response("Permission not found")
    else:
        return success_response("Permission updated successfully", update_permission(db, permission_slug, permission))


@router.delete("/permissions/{permission_slug}")
def delete_permission_route(permission_slug: str, db: Session = Depends(get_db)):
    return delete_permission(db, permission_slug)


# ── Role ↔ Permission assignment endpoints ─────────────────────────────────

@router.post("/{role_slug}/permission/{permission_slug}", response_model=APIResponse[RoleResponse])
def assign_permission_route(role_slug: str, permission_slug: str, db: Session = Depends(get_db)):
    db_role = get_role_by_slug(db, role_slug)
    if not db_role:
        return not_found_response("Role not found")
    db_perm = get_permission_by_slug(db, permission_slug)
    if not db_perm:
        return not_found_response("Permission not found")
    return success_response("Permission assigned successfully", add_permission_to_role(db, db_role, db_perm))


@router.delete("/{role_slug}/permission/{permission_slug}", response_model=APIResponse[RoleResponse])
def remove_permission_route(role_slug: str, permission_slug: str, db: Session = Depends(get_db)):
    db_role = get_role_by_slug(db, role_slug)
    if not db_role:
        return not_found_response("Role not found")
    db_perm = get_permission_by_slug(db, permission_slug)
    if not db_perm:
        return not_found_response("Permission not found")
    return success_response("Permission removed successfully", remove_permission_from_role(db, db_role, db_perm))