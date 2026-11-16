from fastapi import APIRouter
from app.auth.routes.admin_api import router as admin_auth_router
from app.auth.routes.user_api import router as user_auth_router
from app.auth.routes.role_api import router as role_router

router = APIRouter()

router.include_router(admin_auth_router)
router.include_router(user_auth_router)
router.include_router(role_router)
