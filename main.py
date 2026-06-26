from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.db.database import engine, init_db
from app.model import User                  # triggers model registration
from app.auth.routes.admin_api import router as admin_router
# from app.admin.auth import AdminAuth
# from app.admin.views.user_view import UserAdmin
# from app.admin.views.organization_view import OrganizationAdmin

# Create tables
init_db()

app = FastAPI(title=settings.APP_NAME)

# Required for admin session
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(admin_router)


@app.get('/')
def root():
    return {"message": f"{settings.APP_NAME} API is running!"}
