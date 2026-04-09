"""
权限检查依赖
提供统一的认证和授权依赖
"""
from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user_id
from app.core.redis import redis_client
from app.crud.user import user_crud
from app.crud.post import post_crud
from app.models.user import User


async def get_current_user() -> str:
    """获取当前登录用户 ID"""
    return await get_current_user_id()


async def require_admin(user_id: str = Depends(get_current_user)) -> str:
    """要求是管理员用户"""
    is_admin = await user_crud.is_superuser(user_id)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return user_id


async def require_post_owner_or_admin(
    post_id: str,
    user_id: str = Depends(get_current_user)
) -> dict:
    """要求是文章所有者或管理员"""
    post = await post_crud.get_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文章不存在"
        )

    is_admin = await user_crud.is_superuser(user_id)
    if str(post.author_id) != user_id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限操作此文章"
        )

    return {"user_id": user_id, "post": post}


async def check_rate_limit(
    key: str,
    max_attempts: int,
    window_seconds: int
) -> None:
    """检查请求频率限制"""
    is_limited, retry_after = await redis_client.incr_rate_limit(
        key, window_seconds, max_attempts
    )
    if is_limited:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"请求过于频繁，请 {retry_after} 秒后重试"
        )
