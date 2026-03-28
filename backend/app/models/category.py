"""
分类模型
"""
import uuid
from tortoise import fields, models


class Category(models.Model):
    """分类模型"""

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=50, unique=True, description="分类名称")
    slug = fields.CharField(max_length=50, unique=True, description="URL别名")
    description = fields.TextField(null=True, description="分类描述")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
