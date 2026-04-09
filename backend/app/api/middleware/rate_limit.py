"""
限流中间件
基于 IP + 用户名的请求频率限制
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.redis import redis_client


# 创建限流器实例
limiter = Limiter(key_func=get_remote_address)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """自定义限流中间件"""

    LOGIN_MAX_ATTEMPTS = 5  # 5分钟内最多5次失败
    LOGIN_WINDOW_SECONDS = 300  # 5分钟窗口
    REGISTER_MAX_ATTEMPTS = 3  # 5分钟内最多3次注册
    REGISTER_WINDOW_SECONDS = 300

    async def dispatch(self, request: Request, call_next):
        # 只对登录和注册接口限流
        path = request.url.path
        client_ip = get_remote_address(request)

        if path == "/api/v1/auth/login" and request.method == "POST":
            # 获取登录尝试次数
            is_limited, retry_after = await self._check_login_limit(client_ip)
            if is_limited:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"登录尝试过于频繁，请 {retry_after} 秒后重试"
                )

        elif path == "/api/v1/auth/register" and request.method == "POST":
            is_limited, retry_after = await self._check_register_limit(client_ip)
            if is_limited:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"注册过于频繁，请 {retry_after} 秒后重试"
                )

        response = await call_next(request)
        return response

    async def _check_login_limit(self, client_ip: str) -> tuple[bool, int]:
        """检查登录限流"""
        key = f"rate_limit:login:{client_ip}"
        current, exceeded = await redis_client.incr_rate_limit(
            key,
            self.LOGIN_WINDOW_SECONDS,
            self.LOGIN_MAX_ATTEMPTS
        )

        if exceeded:
            ttl = await redis_client.client.ttl(key)
            return True, ttl if ttl > 0 else self.LOGIN_WINDOW_SECONDS

        return False, 0

    async def _check_register_limit(self, client_ip: str) -> tuple[bool, int]:
        """检查注册限流"""
        key = f"rate_limit:register:{client_ip}"
        current, exceeded = await redis_client.incr_rate_limit(
            key,
            self.REGISTER_WINDOW_SECONDS,
            self.REGISTER_MAX_ATTEMPTS
        )

        if exceeded:
            ttl = await redis_client.client.ttl(key)
            return True, ttl if ttl > 0 else self.REGISTER_WINDOW_SECONDS

        return False, 0


async def reset_login_limit(client_ip: str) -> None:
    """登录成功后重置限流计数"""
    key = f"rate_limit:login:{client_ip}"
    await redis_client.reset_rate_limit(key)


def get_client_ip(request: Request) -> str:
    """获取客户端 IP"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
