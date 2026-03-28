"""
评论模型
"""
import uuid
from tortoise import fields, models


class Comment(models.Model):
    """评论模型"""

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    content = fields.TextField(description="评论内容")
    is_approved = fields.BooleanField(default=True, description="是否审核通过")

    # 关联用户（评论者）
    author = fields.ForeignKeyField(
        "models.User",
        related_name="comments",
        on_delete=fields.CASCADE,
        description="评论者"
    )

    # 关联文章
    post = fields.ForeignKeyField(
        "models.Post",
        related_name="comments",
        on_delete=fields.CASCADE,
        description="所属文章"
    )

    # 自关联（回复）
    parent = fields.ForeignKeyField(
        "models.Comment",
        related_name="replies",
        on_delete=fields.CASCADE,
        null=True,
        description="父评论"
    )

    # 时间戳
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
