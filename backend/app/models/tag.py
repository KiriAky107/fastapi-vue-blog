"""
标签模型
"""
import uuid
from tortoise import fields, models


class Tag(models.Model):
    """标签模型"""

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=50, unique=True, description="标签名称")
    slug = fields.CharField(max_length=50, unique=True, description="URL别名")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "tags"
        ordering = ["name"]

    def __str__(self):
        return self.name
