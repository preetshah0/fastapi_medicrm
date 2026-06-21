from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.db.database import engine, init_db
from app.model import User                  # triggers model registration
from app.admin.auth import AdminAuth
from app.admin.views.user_view import UserAdmin

# Create tables
init_db()

app = FastAPI(title=settings.APP_NAME)

# Required for admin session
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Setup admin panel
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title=settings.APP_NAME,
)
admin.add_view(UserAdmin)

@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} API is running!"}