from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.db.schemas.master_options import (
    MasterOptionCreate,
    MasterOptionUpdate,
    MasterOptionResponse,
    MasterOptionDropdownResponse,
    MasterOptionTypeResponse,
)
from app.Enum.MasterOptionType import MasterOptionType
from app.model.MasterOption import Master
from app.owner.controller.masteroption import (
    create_master_option,
    get_master_options,
    get_master_option_by_id,
    get_master_option_dropdown,
    get_master_option_types,
    generate_slug,
    update_master_option,
    delete_master_option,
)
from app.utils.ApiResponse import success_response, error_response, not_found_response
from app.utils.auth_utils import require_permission

router = APIRouter(prefix="/owner/master-options", tags=["master-options"])


@router.get(
    "/types",
    dependencies=[Depends(require_permission("master-options", action="view"))],
    response_model=APIResponse[List[MasterOptionTypeResponse]],
)
def get_master_option_types_route():
    types = get_master_option_types()
    return success_response("Master option types fetched successfully", types)


@router.get(
    "/dropdown/organization/{organization_id}",
    dependencies=[Depends(require_permission("master-options", action="view"))],
    response_model=APIResponse[List[MasterOptionDropdownResponse]],
)
def get_master_option_dropdown_route(
    organization_id: str,
    option_type: MasterOptionType,
    db: Session = Depends(get_db)
):
    options = get_master_option_dropdown(
        db=db,
        organization_id=organization_id,
        option_type=option_type
    )
    return success_response("Master options dropdown fetched successfully", options)


@router.post(
    "/create/{organization_id}",
    dependencies=[Depends(require_permission("master-options", action="create"))],
    response_model=APIResponse[MasterOptionResponse],
)
def create_master_option_route(
    organization_id: str,
    payload: MasterOptionCreate,
    db: Session = Depends(get_db)
):
    slug = generate_slug(payload.name)
    type_value = payload.type.value
    existing = db.query(Master).filter(
        Master.organization_id == organization_id,
        Master.type == type_value,
        Master.slug == slug
    ).first()

    if existing:
        return error_response(f"Master option with name '{payload.name}' already exists for type '{type_value}'.", data="")

    result = create_master_option(db=db, master_option_data=payload, organization_id=organization_id)
    if not result:
        return error_response("Failed to create master option", data="")

    return success_response("Master option created successfully", result)


@router.get(
    "/organization/{organization_id}",
    dependencies=[Depends(require_permission("master-options", action="view"))],
    response_model=APIResponse[List[MasterOptionResponse]],
)
def get_master_options_route(
    organization_id: str,
    option_type: MasterOptionType,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    options = get_master_options(
        db=db, 
        organization_id=organization_id, 
        option_type=option_type,
        is_active=is_active,
        skip=skip,
        limit=limit
    )
    return success_response("Master options fetched successfully", options)


@router.get(
    "/{master_option_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("master-options", action="view"))],
    response_model=APIResponse[MasterOptionResponse],
)
def get_master_option_route(
    master_option_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    master_option = get_master_option_by_id(db=db, master_option_id=master_option_id, organization_id=organization_id)
    if not master_option:
        return not_found_response("Master option not found", data="")
    return success_response("Master option fetched successfully", master_option)


@router.put(
    "/{master_option_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("master-options", action="edit"))],
    response_model=APIResponse[MasterOptionResponse],
)
def update_master_option_route(
    master_option_id: str,
    organization_id: str,
    payload: MasterOptionUpdate,
    db: Session = Depends(get_db)
):
    master_option = get_master_option_by_id(db=db, master_option_id=master_option_id, organization_id=organization_id)
    if not master_option:
        return not_found_response("Master option not found", data="")

    if payload.name is not None:
        new_slug = generate_slug(payload.name)
        target_type = payload.type.value if payload.type else master_option.type
        existing = db.query(Master).filter(
            Master.organization_id == organization_id,
            Master.type == target_type,
            Master.slug == new_slug,
            Master.id != master_option_id
        ).first()
        if existing:
            return error_response(f"Master option with name '{payload.name}' already exists for type '{target_type}'.", data="")

    result = update_master_option(
        db=db,
        master_option_id=master_option_id,
        master_option_data=payload,
        organization_id=organization_id
    )
    if not result:
        return error_response("Failed to update master option", data="")

    return success_response("Master option updated successfully", result)


@router.delete(
    "/{master_option_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("master-options", action="delete"))],
    response_model=APIResponse[str],
)
def delete_master_option_route(
    master_option_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    master_option = get_master_option_by_id(db=db, master_option_id=master_option_id, organization_id=organization_id)
    if not master_option:
        return not_found_response("Master option not found", data="")

    delete_master_option(db=db, master_option_id=master_option_id, organization_id=organization_id)
    return success_response("Master option deleted successfully", data="")

