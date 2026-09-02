from app.utils.auth_utils import get_current_user_id
from app.utils.ApiResponse import *
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from app.model.User import User
from app.model.UserRefreshToken import UserRefreshToken
from app.Enum.UserRole import UserRole
from jose import jwt
from app.utils.auth_utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_user,
    get_user_by_id,
)
from app.db.database import get_db
from fastapi import Depends
from app.core.config import settings


def _get_active_refresh_token(db: Session, token: str) -> UserRefreshToken | None:
    return (
        db.query(UserRefreshToken)
        .filter(
            UserRefreshToken.token == token,
            UserRefreshToken.deleted_at.is_(None),
            (UserRefreshToken.expires_at.is_(None)) | (UserRefreshToken.expires_at > datetime.utcnow()),
        )
        .first()
    )


def login(db: Session, email: str, password: str):
   
    user = authenticate_user(db, email, password)
    if not user or user.role != UserRole.ADMIN.value:
        return unauthorized_response("Invalid admin credentials")

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token({"sub": user.id})

    db.add(
        UserRefreshToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7),
        )
    )
    db.commit()

    return success_response(
        "Admin login successful",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            },
        },
    )


def refresh_token(db: Session, refresh_token_str: str):
    """
    Refresh access token
    Args:
        db (Session): database session
        refresh_token_str (str): refresh token
    Returns:
        JSONResponse: new access token
    """
    if not refresh_token_str:
        return unauthorized_response("Refresh token is required", data = "")

    user_id = None
    try:
        secret_key = settings.REFRESH_TOKEN_SECRET_KEY or settings.SECRET_KEY
        payload = jwt.decode(refresh_token_str, secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
    except Exception:
        return unauthorized_response("Invalid or expired refresh token", data = "")

    if not user_id:
        return unauthorized_response("Invalid refresh token", data = "")

    stored_token = db.query(UserRefreshToken).filter(UserRefreshToken.token == refresh_token_str).first()
    if not stored_token or stored_token.deleted_at is not None:
        return unauthorized_response("Invalid refresh token", data = "")

    if stored_token.expires_at and stored_token.expires_at <= datetime.utcnow():
        db.delete(stored_token)
        db.commit()
        return unauthorized_response("Refresh token has expired", data = "")

    user = get_user_by_id(db, user_id)
    if not user:
        return not_found_response("User not found", data = "")

    if user.role != UserRole.ADMIN.value:
        return unauthorized_response("User is not allowed to refresh admin tokens", data = "")

    access_token = create_access_token({"sub": user.id})
    new_refresh_token = create_refresh_token({"sub": user.id})

    stored_token.token = new_refresh_token
    stored_token.expires_at = datetime.utcnow() + timedelta(days=7)
    db.commit()

    return success_response(
        "Token refreshed successfully",
        data={
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        },
    )


def logout(db: Session, refresh_token_str: str):
   
    if not refresh_token_str:
        return error_response("Refresh token is required", data = "")

    stored_token = db.query(UserRefreshToken).filter(UserRefreshToken.token == refresh_token_str).first()
    if not stored_token:
        return error_response("Invalid refresh token", data = "")

    db.delete(stored_token)
    db.commit()

    return success_response("Logout successful", data = "")


def get_admin_user(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    user = get_user_by_id(db, user_id)
    if not user:
        return HTTP_401_RESPONSE("User not found")

    if user.role != UserRole.ADMIN.value:
        return HTTP_401_RESPONSE("Only admin users may access this resource")

    return success_response(
        "Admin user loaded",
        data={
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "status": user.status,
        },
    )
