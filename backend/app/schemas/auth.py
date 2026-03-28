"""
认证 Schema
"""
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """登录请求 Schema"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")


class RegisterRequest(BaseModel):
    """注册请求 Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class TokenResponse(BaseModel):
    """令牌响应 Schema"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求 Schema"""
    refresh_token: str = Field(..., description="刷新令牌")
