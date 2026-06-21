from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.db.database import session
from app.model.User import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        db: Session = session()
        try:
            user = db.query(User).filter(
                User.email == email,
                User.role == "admin",
                User.status == True
            ).first()

            if not user:
                return False

            if not pwd_context.verify(password, user.password):
                return False

            request.session["admin_id"] = user.id
            request.session["admin_name"] = user.name
            return True
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        if not request.session.get("admin_id"):
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True