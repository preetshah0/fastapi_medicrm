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
    refresh_token as refresh_controller,
    logout as logout_controller,
    get_user_by_email as get_user_controller,
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

    return refresh_controller(db, item.refresh_token)


@router.post('/logout', response_model=LogoutResponse)
def logout(
    item: LogoutRequest,
    db: Session = Depends(get_db),
):
    
    return logout_controller(db, item.refresh_token)


@router.get('/user')
def user(email: str, db: Session = Depends(get_db)):
    
    return get_user_controller(db, email)
