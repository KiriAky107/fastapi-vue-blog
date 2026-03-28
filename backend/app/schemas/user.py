"""
用户 Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """用户基础 Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")


class UserCreate(UserBase):
    """用户创建 Schema"""
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserUpdate(BaseModel):
    """用户更新 Schema"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserInDB(UserBase):
    """用户数据库 Schema"""
    id: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserPublic(UserBase):
    """用户公开信息 Schema"""
    id: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
