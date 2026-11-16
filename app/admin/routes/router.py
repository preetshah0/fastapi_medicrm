from fastapi import APIRouter, Depends
from app.admin.routes.organization_api import router as organization_router
from app.admin.routes.plan_api import router as plan_router
from app.admin.routes.profile_api import router as profile_router
from app.admin.routes.subscription_api import router as subscription_router
from app.admin.routes.payment_api import router as payment_router
from app.utils.auth_utils import get_current_admin

router = APIRouter(dependencies=[Depends(get_current_admin)])

router.include_router(organization_router)
router.include_router(plan_router)
router.include_router(profile_router)
router.include_router(subscription_router)
router.include_router(payment_router)
