"""
用户 API 接口
"""
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserPublic, UserUpdate
from app.crud.user import user_crud
from app.core.security import get_current_user_id
from app.core.logger import app_logger

router = APIRouter(prefix="/users", tags=["用户"])


@router.get("/me", response_model=UserPublic)
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    """获取当前用户信息"""
    user = await user_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user


@router.put("/me", response_model=UserPublic)
async def update_current_user(
    user_update: UserUpdate,
    user_id: str = Depends(get_current_user_id)
):
    """更新当前用户信息"""
    user = await user_crud.update(user_id, **user_update.model_dump(exclude_unset=True))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    app_logger.info(f"User updated: {user.username}")
    return user


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(user_id: str):
    """获取指定用户信息"""
    user = await user_crud.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return user
