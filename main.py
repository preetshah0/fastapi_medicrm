from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.sessions import SessionMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.redis import limiter
from app.core.config import settings, Settings, get_settings
from app.core.scheduler import scheduler, register_jobs
from app.db.database import engine, init_db
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



# Exception Handlers for consistent API responses
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
