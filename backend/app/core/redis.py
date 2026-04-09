"""
Redis 连接模块
提供 Redis 连接和常用操作
"""
import json
from typing import Optional, Any
from datetime import timedelta

import redis.asyncio as redis

from app.core.config import settings


class RedisClient:
    """Redis 客户端封装"""

    _instance: Optional["RedisClient"] = None
    _client: Optional[redis.Redis] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self) -> None:
        """建立 Redis 连接"""
        if self._client is None:
            self._client = redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
            )

    async def close(self) -> None:
        """关闭 Redis 连接"""
        if self._client:
            await self._client.close()
            self._client = None

    @property
    def client(self) -> redis.Redis:
        """获取 Redis 客户端"""
        if self._client is None:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._client

    # ==================== Token 黑名单 ====================

    async def add_to_blacklist(self, token: str, expire_seconds: int) -> None:
        """将 token 加入黑名单"""
        await self.client.setex(
            f"blacklist:{token}",
            expire_seconds,
            "1"
        )

    async def is_token_blacklisted(self, token: str) -> bool:
        """检查 token 是否在黑名单中"""
        result = await self.client.get(f"blacklist:{token}")
        return result is not None

    # ==================== 限流计数 ====================

    async def incr_rate_limit(
        self,
        key: str,
        expire_seconds: int,
        max_attempts: int
    ) -> tuple[int, bool]:
        """
        增加限流计数
        返回: (当前计数, 是否超过限制)
        """
        current = await self.client.incr(key)
        if current == 1:
            # 第一次，设置过期时间
            await self.client.expire(key, expire_seconds)

        return current, current > max_attempts

    async def get_rate_limit_remaining(self, key: str, max_attempts: int) -> int:
        """获取剩余可用次数"""
        current = await self.client.get(key)
        if current is None:
            return max_attempts
        return max(0, max_attempts - int(current))

    async def reset_rate_limit(self, key: str) -> None:
        """重置限流计数"""
        await self.client.delete(key)

    # ==================== 通用操作 ====================

    async def get(self, key: str) -> Optional[str]:
        """获取值"""
        return await self.client.get(key)

    async def set(
        self,
        key: str,
        value: Any,
        expire: Optional[timedelta] = None
    ) -> None:
        """设置值"""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str) -> None:
        """删除键"""
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return await self.client.exists(key) > 0


# 全局实例
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """获取 Redis 客户端"""
    return redis_client
