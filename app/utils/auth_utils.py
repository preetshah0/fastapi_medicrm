from app.Enum.UserRole import UserRole
from datetime import timedelta, datetime
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings
from app.db.database import get_db
from app.model.User import User
from app.utils.ApiResponse import *

# class AuthenticationException(Exception):
#     def __init__(self, message: str, status_code: int = 401):
#         self.message = message
#         self.status_code = status_code
#         super().__init__(message)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    secret_key = settings.REFRESH_TOKEN_SECRET_KEY or settings.SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str, key: str | None = None, token_type: str = "access") -> str | None:
    try:
        if token_type == "refresh":
            secret_key = settings.REFRESH_TOKEN_SECRET_KEY or settings.SECRET_KEY
            payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        else:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

        if key:
            return payload.get(key)
        return payload.get("sub")
    except JWTError as e:
        print(e)
        return None


security = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    user_id = await decode_token(token, token_type="access")

    if not user_id:
        return HTTP_401_RESPONSE("Invalid or expired token")

    return user_id


def get_current_user_object(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        HTTP_401_RESPONSE("User not found")

    if user.role == UserRole.ADMIN.value:
        HTTP_401_RESPONSE("Admin users cannot access this resource")

    if not user.organization_id:
        HTTP_401_RESPONSE("User is not registered to any organization")

    return user


def get_permission_slugs(user: User) -> set[str]:
    if user.role in (UserRole.ADMIN.value, UserRole.OWNER.value):
        return {"*"}
    return {
        perm.slug
        for role in (user.roles or [])
        for perm in (role.permissions or [])
        if getattr(perm, "slug", None)
    }


def require_permission(module: str, action: str = "view"):
    permission = f"{module}.{action}"

    def guard(user: User = Depends(get_current_user_object)) -> User:
        slugs = get_permission_slugs(user)

        if "*" in slugs or permission in slugs:
            return user
        HTTP_403_RESPONSE(f"Access denied. Missing permission: '{permission}'")

    return guard