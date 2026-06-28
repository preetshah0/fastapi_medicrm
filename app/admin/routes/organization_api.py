from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.db.schemas import APIResponse
from app.db.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.auth.controller.role import get_role_by_name
from app.admin.controller.organization import (
    create_organization,
    get_organization,
    update_organization,
    delete_organization,
)
from app.utils.ApiResponse import success_response, not_found_response


router = APIRouter(prefix="/admin/organization", tags=["organization"])


@router.post("/create", response_model=APIResponse[OrganizationResponse])
def create_org(org: OrganizationCreate, db: Session = Depends(get_db)):
    owner_role = get_role_by_name(db, "owner")
    if not owner_role:
        return not_found_response("Role not found")
    
    db_org = create_organization(db=db, organization=org, owner_role=owner_role)
    return success_response("Organization created successfully", db_org)


@router.get("/{ref}", response_model=APIResponse[OrganizationResponse])
def get_org(ref: str, db: Session = Depends(get_db)):
    db_org = get_organization(db=db, ref=ref)
    if not db_org:
        return not_found_response("Organization not found")
    
    return success_response("Organization fetched successfully", db_org)


@router.put("/{ref}", response_model=APIResponse[OrganizationResponse])
def update_org(ref: str, org: OrganizationUpdate, db: Session = Depends(get_db)):
    db_org_check = get_organization(db=db, ref=ref)
    if not db_org_check:
        return not_found_response("Organization not found")

    db_org = update_organization(db=db, db_org=db_org_check, organization=org)
    return success_response("Organization updated successfully", db_org)


@router.delete("/{ref}")
def delete_org(ref: str, db: Session = Depends(get_db)):
    db_org = get_organization(db=db, ref=ref)
    if not db_org:
        return not_found_response("Organization not found")
    
    delete_organization(db=db, db_org=db_org)
    return success_response("Organization deleted successfully", data="")

