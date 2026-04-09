"""
数据库模块
Tortoise-ORM 初始化配置
"""
from contextlib import asynccontextmanager
from tortoise import Tortoise

from app.core.config import settings
from app.core.logger import app_logger


async def init_db():
    """初始化数据库连接"""
    app_logger.info("Initializing database connection...")

    await Tortoise.init(
        db_url=settings.DATABASE_URL_ASYNC,
        modules={
            "models": [
                "app.models.user",
                "app.models.post",
                "app.models.category",
                "app.models.tag",
                "app.models.comment",
            ]
        },
        use_tz=False,  # 使用 UTC 时间
        timezone="Asia/Shanghai",  # 使用上海时区
    )

    # 生成 schema
    await Tortoise.generate_schemas()
    app_logger.info("Database connection established")


async def close_db():
    """关闭数据库连接"""
    app_logger.info("Closing database connection...")
    await Tortoise.close_connections()
    app_logger.info("Database connection closed")


@asynccontextmanager
async def with_transaction():
    """事务上下文管理器"""
    connection = Tortoise.get_connection("default")
    try:
        async with connection.begin():
            yield
    except Exception:
        await connection.rollback()
        raise
