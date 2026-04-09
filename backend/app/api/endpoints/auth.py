"""
认证 API 接口
"""
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.security import OAuth2PasswordBearer

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, RefreshTokenRequest
from app.schemas.user import UserPublic
from app.crud.user import user_crud
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    decode_token_sync,
    revoke_token,
)
from app.core.logger import app_logger
from app.api.middleware.rate_limit import get_client_ip, reset_login_limit

router = APIRouter(prefix="/auth", tags=["认证"])

# OAuth2 scheme for logout
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """用户注册"""
    # 使用统一的错误信息，不暴露具体原因
    generic_error = "注册失败，请稍后重试"

    # 检查用户名是否存在（但不明确告知）
    if await user_crud.get_by_username(request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=generic_error
        )

    # 检查邮箱是否存在（但不明确告知）
    if await user_crud.get_by_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=generic_error
        )

    # 创建用户
    try:
        user = await user_crud.create(
            username=request.username,
            email=request.email,
            password=request.password
        )
        app_logger.info(f"New user registered: {user.username}")
        return user
    except Exception as e:
        app_logger.error(f"Registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=generic_error
        )


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, request: Request):
    """用户登录"""
    username_or_email = login_data.username
    password = login_data.password
    client_ip = get_client_ip(request)

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

    # 登录成功，重置限流计数
    await reset_login_limit(client_ip)

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
    # 检查刷新 token 是否在黑名单
    try:
        payload = decode_token_sync(request.refresh_token)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌"
        )

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
    new_refresh_token = create_refresh_token(token_data)

    # 将旧的刷新 token 加入黑名单
    await revoke_token(request.refresh_token)

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """用户登出，撤销 token"""
    if token:
        await revoke_token(token)
    return {"message": "登出成功"}
