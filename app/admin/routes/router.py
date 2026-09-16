from fastapi import APIRouter, Depends
from app.admin.routes.organization_api import router as organization_router
from app.admin.routes.plan_api import router as plan_router
from app.auth.controller.admin_auth import get_admin_user

router = APIRouter(dependencies=[Depends(get_admin_user)])

router.include_router(organization_router)
router.include_router(plan_router)
