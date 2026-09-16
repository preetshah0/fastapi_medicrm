from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.redis import limiter
from app.core.config import settings, Settings, get_settings
from app.core.scheduler import scheduler, register_jobs
from app.db.database import engine, init_db
from app.utils.ApiResponse import validation_error_response
# from app.db.seeder.PermissionSeeder import seed_permissions
from app.model import User                 
# from app.utils.auth_utils import AuthenticationException
from app.auth.routes.router import router as auth_router
from app.admin.routes.router import router as admin_router
from app.owner.routes.router import router as owner_router
# from app.admin.auth import AdminAuth
# from app.admin.views.user_view import UserAdmin
# from app.admin.views.organization_view import OrganizationAdmin

# Create tables
init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # seed_permissions() #Only uncomment if you want to seed permissions
    register_jobs()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    debug=(settings.APP_ENV == "local" or settings.APP_DEBUG)
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers for consistent API responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return validation_error_response(
        message="Validation failed",
        data=exc.errors(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """
    Handle HTTP exceptions and return consistent API response format.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "success": False,
            "message": exc.detail if isinstance(exc.detail, str) else "Request failed",
            "data": None if isinstance(exc.detail, str) else exc.detail,
        }),
    )

# @app.exception_handler(AuthenticationException)
# async def authentication_exception_handler(request, exc: AuthenticationException):
#     """
#     Handle authentication exceptions and return consistent API response format
#     """
#     return JSONResponse(
#         status_code=exc.status_code,
#         content=jsonable_encoder({
#             "success": False,
#             "message": exc.message,
#             "data": None,
#         }),
#     )


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(owner_router)


@app.get('/')
def root(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.APP_NAME,
        "app_env": settings.APP_ENV,
        "app_debug": settings.APP_DEBUG,
        "message": f"{settings.APP_NAME} API is running!"
    }
