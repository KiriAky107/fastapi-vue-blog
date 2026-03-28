"""
评论 Schema
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    """评论基础 Schema"""
    content: str = Field(..., min_length=1, description="评论内容")


class CommentCreate(CommentBase):
    """评论创建 Schema"""
    post_id: str = Field(..., description="文章ID")
    parent_id: Optional[str] = Field(None, description="父评论ID")


class CommentUpdate(BaseModel):
    """评论更新 Schema"""
    content: Optional[str] = Field(None, min_length=1)


class CommentAuthor(BaseModel):
    """评论作者 Schema"""
    id: str
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class CommentResponse(CommentBase):
    """评论响应 Schema"""
    id: str
    author: CommentAuthor
    post_id: str
    parent_id: Optional[str] = None
    is_approved: bool
    created_at: datetime
    updated_at: datetime
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    """评论列表响应 Schema"""
    items: List[CommentResponse]
    total: int
    page: int
    page_size: int
