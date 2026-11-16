from fastapi import APIRouter
from app.webhook.routes.stripe_api import router as stripe_router

router = APIRouter(prefix="/webhook")
router.include_router(stripe_router)
