"""
FastAPI 应用入口
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.redis import redis_client
from app.core.logger import app_logger
from app.api.api import api_router
from app.api.middleware.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    app_logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}...")

    # 初始化数据库
    await init_db()

    # 连接 Redis
    await redis_client.connect()
    app_logger.info("Redis connected")

    yield

    # 关闭时
    app_logger.info("Shutting down...")
    await redis_client.close()
    await close_db()


def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="ACG 风格博客系统 API",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )

    # 配置 CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 添加限流中间件
    app.add_middleware(RateLimitMiddleware)

    # 注册路由
    app.include_router(api_router)

    # 健康检查
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "app": settings.APP_NAME}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
