"""
文章 API 接口
"""
import math
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostListResponse,
    TagCreate,
    TagResponse,
    CategoryCreate,
    CategoryResponse
)
from app.schemas.post import AuthorResponse
from app.crud.post import post_crud
from app.crud.category import category_crud
from app.crud.tag import tag_crud
from app.crud.user import user_crud
from app.core.security import get_current_user_id
from app.core.logger import app_logger

router = APIRouter(prefix="/posts", tags=["文章"])
category_router = APIRouter(prefix="/categories", tags=["分类"])
tag_router = APIRouter(prefix="/tags", tags=["标签"])


# ==================== 文章接口 ====================

@router.get("", response_model=PostListResponse)
async def get_posts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query("published", description="文章状态"),
    category_id: Optional[str] = Query(None, description="分类ID"),
    tag_id: Optional[str] = Query(None, description="标签ID")
):
    """获取文章列表"""
    posts, total = await post_crud.get_all(
        page=page,
        page_size=page_size,
        status=status,
        category_id=category_id,
        tag_id=tag_id
    )

    return PostListResponse(
        items=posts,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 0
    )


@router.get("/hot", response_model=list[PostResponse])
async def get_hot_posts(limit: int = Query(10, ge=1, le=50)):
    """获取热门文章"""
    posts = await post_crud.get_hot_posts(limit=limit)
    return posts


@router.get("/recent", response_model=list[PostResponse])
async def get_recent_posts(limit: int = Query(10, ge=1, le=50)):
    """获取最新文章"""
    posts = await post_crud.get_recent_posts(limit=limit)
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    """获取文章详情"""
    post = await post_crud.get_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    # 增加浏览量
    await post_crud.increment_view_count(post_id)

    return post


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    user_id: str = Depends(get_current_user_id)
):
    """创建文章"""
    # 检查 slug 是否已存在
    if await post_crud.get_by_slug(post_data.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL别名已存在"
        )

    post = await post_crud.create(
        author_id=user_id,
        **post_data.model_dump()
    )

    app_logger.info(f"Post created: {post.title} by user {user_id}")
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_data: PostUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """更新文章"""
    post = await post_crud.get_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    # 检查权限
    if str(post.author_id) != user_id:
        is_admin = await user_crud.is_superuser(user_id)
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限修改此文章"
            )

    updated_post = await post_crud.update(
        post_id,
        **post_data.model_dump(exclude_unset=True)
    )

    app_logger.info(f"Post updated: {updated_post.title}")
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """删除文章"""
    post = await post_crud.get_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    # 检查权限
    if str(post.author_id) != user_id:
        is_admin = await user_crud.is_superuser(user_id)
        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限删除此文章"
            )

    await post_crud.delete(post_id)
    app_logger.info(f"Post deleted: {post_id}")


# ==================== 分类接口 ====================

@category_router.get("", response_model=list[CategoryResponse])
async def get_categories():
    """获取所有分类"""
    return await category_crud.get_all()


@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: str):
    """获取分类详情"""
    category = await category_crud.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    return category


@category_router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    user_id: str = Depends(get_current_user_id)
):
    """创建分类"""
    # 检查权限
    is_admin = await user_crud.is_superuser(user_id)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    # 检查 slug 是否已存在
    if await category_crud.get_by_slug(category_data.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL别名已存在"
        )

    category = await category_crud.create(**category_data.model_dump())
    app_logger.info(f"Category created: {category.name}")
    return category


@category_router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: str,
    category_data: CategoryCreate,
    user_id: str = Depends(get_current_user_id)
):
    """更新分类"""
    is_admin = await user_crud.is_superuser(user_id)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    category = await category_crud.update(category_id, **category_data.model_dump())
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分类不存在"
        )
    return category


@category_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """删除分类"""
    is_admin = await user_crud.is_superuser(user_id)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    await category_crud.delete(category_id)


# ==================== 标签接口 ====================

@tag_router.get("", response_model=list[TagResponse])
async def get_tags():
    """获取所有标签"""
    return await tag_crud.get_all()


@tag_router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(tag_id: str):
    """获取标签详情"""
    tag = await tag_crud.get_by_id(tag_id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在"
        )
    return tag


@tag_router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    user_id: str = Depends(get_current_user_id)
):
    """创建标签"""
    # 检查 slug 是否已存在
    if await tag_crud.get_by_slug(tag_data.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL别名已存在"
        )

    tag = await tag_crud.create(**tag_data.model_dump())
    app_logger.info(f"Tag created: {tag.name}")
    return tag
