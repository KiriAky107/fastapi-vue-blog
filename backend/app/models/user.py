"""
用户模型
"""
import uuid
from datetime import datetime
from tortoise import fields, models


class User(models.Model):
    """用户模型"""

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    username = fields.CharField(max_length=50, unique=True, description="用户名")
    email = fields.CharField(max_length=255, unique=True, description="邮箱")
    password_hash = fields.CharField(max_length=255, description="密码哈希")
    avatar = fields.CharField(max_length=500, null=True, description="头像URL")
    bio = fields.TextField(null=True, description="个人简介")
    is_active = fields.BooleanField(default=True, description="是否激活")
    is_superuser = fields.BooleanField(default=False, description="是否超级用户")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.username
