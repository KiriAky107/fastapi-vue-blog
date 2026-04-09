"""
常量定义
"""
from enum import Enum


class PostStatus(str, Enum):
    """文章状态"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class UserStatus(str, Enum):
    """用户状态"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"


# 分页默认值
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# 文章内容限制
MAX_TITLE_LENGTH = 200
MAX_SLUG_LENGTH = 200
MAX_CONTENT_LENGTH = 100000  # 100KB
MAX_SUMMARY_LENGTH = 500

# 用户名密码限制
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 128
MIN_USERNAME_LENGTH = 2
MAX_USERNAME_LENGTH = 50
