"""
评论 API 接口
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentListResponse
)
from app.crud.comment import comment_crud
from app.crud.post import post_crud
from app.core.security import get_current_user_id
from app.core.logger import app_logger

router = APIRouter(prefix="/comments", tags=["评论"])


@router.get("/post/{post_id}", response_model=CommentListResponse)
async def get_post_comments(
    post_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    approved_only: bool = Query(True, description="仅显示已审核评论")
):
    """获取文章的所有评论"""
    # 检查文章是否存在
    post = await post_crud.get_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    comments, total = await comment_crud.get_by_post(
        post_id=post_id,
        page=page,
        page_size=page_size,
        approved_only=approved_only
    )

    return CommentListResponse(
        items=comments,
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    user_id: str = Depends(get_current_user_id)
):
    """创建评论"""
    # 检查文章是否存在
    post = await post_crud.get_by_id(comment_data.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    # 如果是回复，检查父评论是否存在
    if comment_data.parent_id:
        parent = await comment_crud.get_by_id(comment_data.parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父评论不存在"
            )
        if str(parent.post_id) != comment_data.post_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="父评论不属于该文章"
            )

    comment = await comment_crud.create(
        content=comment_data.content,
        author_id=user_id,
        post_id=comment_data.post_id,
        parent_id=comment_data.parent_id
    )

    app_logger.info(f"Comment created on post {comment_data.post_id} by user {user_id}")
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """更新评论"""
    comment = await comment_crud.get_by_id(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 检查权限（只能修改自己的评论）
    if str(comment.author_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改此评论"
        )

    updated_comment = await comment_crud.update(
        comment_id,
        **comment_data.model_dump(exclude_unset=True)
    )

    app_logger.info(f"Comment updated: {comment_id}")
    return updated_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: str,
    user_id: str = Depends(get_current_user_id)
):
    """删除评论"""
    comment = await comment_crud.get_by_id(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )

    # 检查权限（只能删除自己的评论）
    if str(comment.author_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限删除此评论"
        )

    await comment_crud.delete(comment_id)
    app_logger.info(f"Comment deleted: {comment_id}")
