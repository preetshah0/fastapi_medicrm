from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.response import APIResponse
from app.Enum import SaleType, SalesStatus, SalePaymentStatus
from app.db.schemas import (
    SaleCreate,
    SaleUpdate,
    DispenseSaleRequest,
    SaleResponse,
    SaleBranchResponse,
    SaleEnumResponse,
    SalePrescriptionResponse,
)
from app.owner.controller.sale import (
    create_sale,
    get_sales,
    get_sale_by_id,
    update_sale,
    delete_sale,
    dispense_sale,
    cancel_sale,
    get_branch,
    get_prescription,
    get_sale_types,
    get_sale_payment_method_types,
    get_sale_payment_status_types,
    get_sales_status_types,
)
from app.model.Branch import Branch
from app.utils.ApiResponse import success_response, error_response, not_found_response
from app.utils.auth_utils import require_permission

router = APIRouter(prefix="/owner/sales", tags=["sales"])


@router.post(
    "/create",
    dependencies=[Depends(require_permission("sales", action="create"))],
    response_model=APIResponse[SaleResponse],
)
def create_sale_route(
    payload: SaleCreate,
    db: Session = Depends(get_db)
):
    branch = db.query(Branch).filter(Branch.id == payload.branch_id).first()
    if not branch:
        return error_response("Invalid branch selected", data=None)
    sales_type_val = payload.sales_type.value if hasattr(payload.sales_type, "value") else str(payload.sales_type)
    if sales_type_val == SaleType.INTERNAL.value or sales_type_val == "internal":
        if not payload.patient_id:
            return error_response("Patient ID is required for internal sales", data=None)

    if not payload.items or len(payload.items) == 0:
        return error_response("Sale must contain at least one item", data=None)

    try:
        result = create_sale(db=db, sale_data=payload)
        if not result:
            return error_response("Failed to create sale record", data=None)
        return success_response("Sale created successfully", result)
    except HTTPException as e:
        return error_response(e.detail, data=None)
    except Exception as e:
        return error_response(str(e), data=None)


@router.get(
    "/organization/{organization_id}",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[List[SaleResponse]],
)
def get_sales_route(
    organization_id: str,
    branch_id: Optional[str] = Query(None),
    patient_id: Optional[str] = Query(None),
    sales_status: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    sales_type: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    try:
        results = get_sales(
            db=db,
            organization_id=organization_id,
            branch_id=branch_id,
            patient_id=patient_id,
            sales_status=sales_status,
            payment_status=payment_status,
            sales_type=sales_type,
            search=search,
            skip=skip,
            limit=limit,
        )
        return success_response("Sales fetched successfully", results)
    except Exception as e:
        return error_response(str(e), data=None)


@router.get(
    "/{sale_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[SaleResponse],
)
def get_sale_route(
    sale_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    try:
        result = get_sale_by_id(db=db, sale_id=sale_id, organization_id=organization_id)
        if not result:
            return not_found_response("Sale record not found", data=None)
        return success_response("Sale fetched successfully", result)
    except Exception as e:
        return error_response(str(e), data=None)


@router.put(
    "/{sale_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("sales", action="edit"))],
    response_model=APIResponse[SaleResponse],
)
def update_sale_route(
    sale_id: str,
    organization_id: str,
    payload: SaleUpdate,
    db: Session = Depends(get_db)
):
    existing = get_sale_by_id(db=db, sale_id=sale_id, organization_id=organization_id)
    if not existing:
        return not_found_response("Sale record not found", data=None)

    try:
        result = update_sale(db=db, sale_id=sale_id, sale_data=payload, organization_id=organization_id)
        return success_response("Sale updated successfully", result)
    except HTTPException as e:
        return error_response(e.detail, data=None)
    except Exception as e:
        return error_response(str(e), data=None)


@router.post(
    "/{sale_id}/dispense",
    dependencies=[Depends(require_permission("sales", action="edit"))],
    response_model=APIResponse[SaleResponse],
)
@router.post(
    "/{sale_id}/organization/{organization_id}/dispense",
    dependencies=[Depends(require_permission("sales", action="edit"))],
    response_model=APIResponse[SaleResponse],
)
def dispense_sale_route(
    sale_id: str,
    payload: DispenseSaleRequest,
    organization_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    existing = get_sale_by_id(db=db, sale_id=sale_id, organization_id=organization_id)
    if not existing:
        return not_found_response("Sale record not found", data=None)

    if existing.sales_status == SalesStatus.DISPENSED.value or existing.sales_status == "dispensed":
        return error_response("Sale has already been dispensed", data=None)

    try:
        result = dispense_sale(
            db=db,
            sale_id=sale_id,
            payment_method=payload.payment_method,
            notes=payload.notes,
            organization_id=organization_id,
        )
        return success_response("Sale dispensed and payment completed successfully", result)
    except HTTPException as e:
        return error_response(e.detail, data=None)
    except Exception as e:
        return error_response(str(e), data=None)


@router.post(
    "/{sale_id}/cancel",
    dependencies=[Depends(require_permission("sales", action="edit"))],
    response_model=APIResponse[SaleResponse],
)
@router.post(
    "/{sale_id}/organization/{organization_id}/cancel",
    dependencies=[Depends(require_permission("sales", action="edit"))],
    response_model=APIResponse[SaleResponse],
)
def cancel_sale_route(
    sale_id: str,
    organization_id: Optional[str] = None,
    notes: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    existing = get_sale_by_id(db=db, sale_id=sale_id, organization_id=organization_id)
    if not existing:
        return not_found_response("Sale record not found", data=None)

    if existing.sales_status in [SalesStatus.CANCELLED.value, "cancelled"]:
        return error_response("Sale is already cancelled", data=None)

    if existing.sales_status in [SalesStatus.DISPENSED.value, "dispensed"] or existing.payment_status in [SalePaymentStatus.PAID.value, "paid"]:
        return error_response("Dispensed or paid sales cannot be cancelled", data=None)

    try:
        result = cancel_sale(
            db=db,
            sale_id=sale_id,
            organization_id=organization_id,
            notes=notes,
        )
        return success_response("Sale cancelled and inventory restored successfully", result)
    except HTTPException as e:
        return error_response(e.detail, data=None)
    except Exception as e:
        return error_response(str(e), data=None)


@router.delete(
    "/{sale_id}/organization/{organization_id}",
    dependencies=[Depends(require_permission("sales", action="delete"))],
    response_model=APIResponse[dict],
)
def delete_sale_route(
    sale_id: str,
    organization_id: str,
    db: Session = Depends(get_db)
):
    existing = get_sale_by_id(db=db, sale_id=sale_id, organization_id=organization_id)
    if not existing:
        return not_found_response("Sale record not found", data=None)

    try:
        delete_sale(db=db, sale_id=sale_id, organization_id=organization_id)
        return success_response("Sale deleted successfully", {"id": sale_id})
    except HTTPException as e:
        return error_response(e.detail, data=None)
    except Exception as e:
        return error_response(str(e), data=None)


# Dropdown / Enum helper routes
@router.get(
    "/branches",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[List[SaleBranchResponse]],
)
def get_sale_branches(
    organization_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        results = get_branch(db=db, organization_id=organization_id)
        return success_response("Branches fetched successfully", results)
    except Exception as e:
        return error_response(str(e), data=None)


@router.get(
    "/prescriptions",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[List[SalePrescriptionResponse]],
)
def get_sale_prescriptions(
    organization_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        results = get_prescription(db=db, organization_id=organization_id)
        return success_response("Prescriptions fetched successfully", results)
    except Exception as e:
        return error_response(str(e), data=None)


@router.get(
    "/types",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[List[SaleEnumResponse]],
)
def get_sale_types_route():
    return success_response("Sale types fetched successfully", get_sale_types())


@router.get(
    "/payment-methods",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[List[SaleEnumResponse]],
)
def get_sale_payment_methods_route():
    return success_response("Payment methods fetched successfully", get_sale_payment_method_types())


@router.get(
    "/payment-statuses",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[List[SaleEnumResponse]],
)
def get_sale_payment_statuses_route():
    return success_response("Payment statuses fetched successfully", get_sale_payment_status_types())


@router.get(
    "/statuses",
    dependencies=[Depends(require_permission("sales", action="view"))],
    response_model=APIResponse[List[SaleEnumResponse]],
)
def get_sales_statuses_route():
    return success_response("Sales statuses fetched successfully", get_sales_status_types())

