"""
API 路由汇总
"""
from fastapi import APIRouter
from app.api.endpoints import auth, users, posts, comments

api_router = APIRouter(prefix="/api/v1")

# 注册各模块路由
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(posts.router)
api_router.include_router(posts.category_router)
api_router.include_router(posts.tag_router)
api_router.include_router(comments.router)
