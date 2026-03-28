"""
文章 Schema
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class TagBase(BaseModel):
    """标签基础 Schema"""
    name: str = Field(..., min_length=1, max_length=50, description="标签名")
    slug: str = Field(..., min_length=1, max_length=50, description="URL别名")


class TagCreate(TagBase):
    """标签创建 Schema"""
    pass


class TagResponse(TagBase):
    """标签响应 Schema"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    """分类基础 Schema"""
    name: str = Field(..., min_length=1, max_length=50, description="分类名")
    slug: str = Field(..., min_length=1, max_length=50, description="URL别名")
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """分类创建 Schema"""
    pass


class CategoryResponse(CategoryBase):
    """分类响应 Schema"""
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    """文章基础 Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="标题")
    slug: str = Field(..., min_length=1, max_length=200, description="URL别名")
    content: str = Field(..., description="文章内容")
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[str] = None
    status: str = Field(default="draft", description="状态: draft/published/archived")


class PostCreate(PostBase):
    """文章创建 Schema"""
    tag_ids: Optional[List[str]] = []
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class PostUpdate(BaseModel):
    """文章更新 Schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[str] = None
    tag_ids: Optional[List[str]] = None
    status: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class AuthorResponse(BaseModel):
    """作者响应 Schema"""
    id: str
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    """文章响应 Schema"""
    id: str
    author: AuthorResponse
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []
    view_count: int
    like_count: int
    comment_count: int
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    """文章列表响应 Schema"""
    items: List[PostResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
