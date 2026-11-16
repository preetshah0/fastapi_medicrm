from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.redis import limiter
from app.db.database import get_db
from app.db.schemas.auth import (
    LogoutRequest,
    TokenRefreshRequest,
    AdminLoginResponse,
    TokenRefreshResponse,
    LogoutResponse,
)
from app.auth.controller.user_auth import (
    login as login_controller,
    refresh_token,
    logout,
    get_current_user_json,
)

router = APIRouter(prefix="/user/auth", tags=["user_auth"])


@router.post('/login', response_model=AdminLoginResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    return login_controller(db, email, password)


@router.post('/refresh', response_model=TokenRefreshResponse)
def refresh(
    item: TokenRefreshRequest,
    db: Session = Depends(get_db),
):
    return refresh_token(db, item.refresh_token)


@router.post('/logout', response_model=LogoutResponse)
def logout(
    item: LogoutRequest,
    db: Session = Depends(get_db),
):
    return logout(db, item.refresh_token)


@router.get('/user')
def user(user_data=Depends(get_current_user_json)):
    return user_data

