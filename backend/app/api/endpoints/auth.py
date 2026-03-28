"""
认证 API 接口
"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, RefreshTokenRequest
from app.schemas.user import UserPublic
from app.crud.user import user_crud
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.logger import app_logger

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """用户注册"""
    # 检查用户名是否存在
    if await user_crud.get_by_username(request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否存在
    if await user_crud.get_by_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )

    # 创建用户
    user = await user_crud.create(
        username=request.username,
        email=request.email,
        password=request.password
    )

    app_logger.info(f"New user registered: {user.username}")
    return user


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """用户登录"""
    username_or_email = login_data.username
    password = login_data.password

    # 验证用户
    user = await user_crud.authenticate(username_or_email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    # 生成令牌
    token_data = {"sub": str(user.id), "username": user.username}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    app_logger.info(f"User logged in: {user.username}")
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """刷新令牌"""
    payload = decode_token(request.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )

    user_id = payload.get("sub")
    username = payload.get("username")

    # 生成新令牌
    token_data = {"sub": user_id, "username": username}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout():
    """用户登出（前端清除令牌即可）"""
    return {"message": "登出成功"}
