"""
统一响应模式
"""
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """成功响应"""
    code: int = 200
    message: str = "Success"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """错误响应"""
    code: int = 400
    message: str = "An error occurred"
    detail: Optional[str] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int = 0


def success_response(data: T = None, message: str = "Success") -> SuccessResponse[T]:
    """创建成功响应"""
    return SuccessResponse(code=200, message=message, data=data)


def error_response(message: str = "An error occurred", code: int = 400, detail: str = None) -> ErrorResponse:
    """创建错误响应"""
    return ErrorResponse(code=code, message=message, detail=detail)
