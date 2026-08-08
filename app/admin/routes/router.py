from fastapi import APIRouter
from app.admin.routes.organization_api import router as organization_router

router = APIRouter()

router.include_router(organization_router)
