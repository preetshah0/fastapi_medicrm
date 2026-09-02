from pydantic import BaseModel, Field
from typing import Optional


class AdminLoginRequest(BaseModel):
    email: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str = Field(..., example="your-refresh-token")


class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., example="your-refresh-token")


class AdminLoginResponse(BaseModel):
    message: str
    data: dict


class TokenRefreshResponse(BaseModel):
    message: str
    data: dict


class LogoutResponse(BaseModel):
    message: str
    data: dict
