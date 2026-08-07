from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.model.User import User
from app.model.Role import Roles
from app.db.database import get_db, session as db_session
from app.db.schemas import APIResponse, BranchCreate, BranchResponse, BranchUpdate
from app.db.schemas.branch import BranchUserAssignRequest, BranchUserResponse
from app.model.Organization import Organization
from app.model.Branch import Branch
from app.owner.controller.branch import (
    create_branch,
    get_branch,
    get_branches_by_organization,
    update_branch,
    delete_branch,
    assign_users_to_branch,
    get_users_by_branch
)
from app.utils.ApiResponse import success_response, error_response, not_found_response

router = APIRouter(prefix="/owner/branch", tags=["branch"])


def get_organization_examples():
    """Dynamically fetch organization names from the organization table for Swagger UI dropdown."""
    try:
        db = db_session()
        orgs = db.query(Organization).all()
        examples = {}
        for org in orgs:
            examples[f"{org.organization_name} ({org.ref})"] = {"value": org.id}
        db.close()
        if not examples:
            examples["Sample Org (Fallback)"] = {"value": "d3b07384-d113-48b2-9a3d-39294e7724a1"}
        return examples
    except Exception:
        return {"Sample Org (Fallback)": {"value": "d3b07384-d113-48b2-9a3d-39294e7724a1"}}


@router.post("/create", response_model=APIResponse[BranchResponse])
def create_branch_route(
branch_data: BranchCreate,
    organization_id: str = Query(
        ...,
        description="Select an Organization from the dynamic dropdown",
        openapi_examples=get_organization_examples(),
    ),
    db: Session = Depends(get_db),
):
    db_org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not db_org:
        return error_response("Organization not found", data="")

    db_branch = db.query(Branch).filter(Branch.branch_email == branch_data.branch_email).first()
    if db_branch:
        return error_response("Branch already exists", data="")

    return success_response(
        "Branch created successfully",
        create_branch(db=db, organization_id=organization_id, branch_data=branch_data),
    )


@router.get("/{branch_id}", response_model=APIResponse[BranchResponse])
def get_branch_route(branch_id: str, db: Session = Depends(get_db)):
    db_branch = get_branch(db=db, branch_id=branch_id)
    if not db_branch:
        return not_found_response("Branch not found")

    return success_response("Branch fetched successfully", db_branch)


@router.get("/organization/{organization_id}", response_model=APIResponse[list[BranchResponse]])
def get_branches_by_organization_route(
    organization_id: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    db_org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not db_org:
        return error_response("Organization not found", data="")

    branches = get_branches_by_organization(db=db, organization_id=organization_id, skip=skip, limit=limit)
    return success_response("Branches fetched successfully", branches)


@router.put("/{branch_id}", response_model=APIResponse[BranchResponse])
def update_branch_route(
    branch_id: str,
    branch_data: BranchUpdate,
    db: Session = Depends(get_db),
):
    db_branch = get_branch(db=db, branch_id=branch_id)
    if not db_branch:
        return not_found_response("Branch not found")

    if branch_data.branch_email:
        db_branch_with_email = db.query(Branch).filter(Branch.branch_email == branch_data.branch_email, Branch.id != branch_id).first()
        if db_branch_with_email:
            return error_response("Branch already exists with this email", data="")
    
    updated_branch = update_branch(db=db, branch_id=branch_id, branch_data=branch_data)
    return success_response("Branch updated successfully", updated_branch)


@router.delete("/{branch_id}")
def delete_branch_route(branch_id: str, db: Session = Depends(get_db)):
    db_branch = get_branch(db=db, branch_id=branch_id)
    if not db_branch:
        return not_found_response("Branch not found")

    delete_branch(db=db, branch_id=branch_id)
    return success_response("Branch deleted successfully", data="")


@router.post("/assign-users", response_model=APIResponse[list[BranchUserResponse]])
def assign_users_to_branches_route(
    payload: BranchUserAssignRequest,
    db: Session = Depends(get_db),
):
    branch_id = payload.branch_id
    db_branch = get_branch(db=db, branch_id=branch_id)
    if not db_branch:
        return not_found_response("Branch not found", data="")

    valid_assignments = []
    for entry in payload.users:
        if not entry.user_id or not entry.role_id:
            return not_found_response("Each user assignment must include user and role", data="")
        
        db_user = db.query(User).filter(User.id == entry.user_id).first()
        if not db_user:
            return not_found_response(f"User not found: {entry.user_id}", data="")
            
        if db_user.organization_id != db_branch.organization_id:
            return error_response(f"User {db_user.name} does not belong to the branch's organization", data="")
            
        db_role = db.query(Roles).filter(Roles.id == entry.role_id).first()
        if not db_role:
            return not_found_response(f"Role not found: {db_role.name}", data="")
            
        valid_assignments.append((db_user, db_role))

    result = assign_users_to_branch(
        db=db,
        db_branch=db_branch,
        users_roles=valid_assignments,
        status=payload.status,
    )

    return success_response("Users assigned to branch successfully", result)


@router.get("/{branch_id}/users", response_model=APIResponse[list[BranchUserResponse]])
def users_branch_route(
    branch_id: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    db_branch = get_branch(db=db, branch_id=branch_id)
    if not db_branch:
        return not_found_response("Branch not found")

    users = get_users_by_branch(db=db, branch_id=branch_id, skip=skip, limit=limit)
    if not users:
        return not_found_response("No users found in this branch", data=[])
        
    return success_response("Users fetched successfully", data=users)
