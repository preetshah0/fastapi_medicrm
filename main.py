from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.core.scheduler import scheduler, register_jobs
from app.db.database import engine, init_db
from app.model import User                  # triggers model registration
from app.utils.auth_utils import AuthenticationException
from app.auth.routes.admin_api import router as admin_router
from app.auth.routes.user_api import router as user_router
from app.auth.routes.role_api import router as role_router
from app.owner.routes.team_api import router as team_router
from app.admin.routes.organization_api import router as organization_router
from app.owner.routes.branch_api import router as branch_router
from app.owner.routes.medical_api import router as medical_reps_router
from app.owner.routes.supplier_api import router as supplier_router
from app.owner.routes.patient_api import router as patient_router, notes_router, reports_router
from app.owner.routes.appointment_api import router as appointment_router
# from app.admin.auth import AdminAuth
# from app.admin.views.user_view import UserAdmin
# from app.admin.views.organization_view import OrganizationAdmin

# Create tables
init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_jobs()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Required for admin session
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


# Exception Handlers for consistent API responses
@app.exception_handler(AuthenticationException)
async def authentication_exception_handler(request, exc: AuthenticationException):
    """
    Handle authentication exceptions and return consistent API response format
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "success": False,
            "message": exc.message,
            "data": None,
        }),
    )


app.include_router(admin_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(team_router)
app.include_router(organization_router)
app.include_router(branch_router)
app.include_router(medical_reps_router)
app.include_router(supplier_router)
app.include_router(patient_router)
app.include_router(notes_router)
app.include_router(reports_router)
app.include_router(appointment_router)


@app.get('/')
def root():
    return {"message": f"{settings.APP_NAME} API is running!"}
