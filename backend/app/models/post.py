"""
文章模型
"""
import uuid
from datetime import datetime
from tortoise import fields, models


class Post(models.Model):
    """文章模型"""

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.CharField(max_length=200, description="文章标题")
    slug = fields.CharField(max_length=200, unique=True, description="URL别名")
    content = fields.TextField(description="文章内容(Markdown)")
    summary = fields.TextField(null=True, description="文章摘要")
    cover_image = fields.CharField(max_length=500, null=True, description="封面图片URL")

    # 关联用户（作者）
    author = fields.ForeignKeyField(
        "models.User",
        related_name="posts",
        on_delete=fields.CASCADE,
        description="作者"
    )

    # 关联分类
    category = fields.ForeignKeyField(
        "models.Category",
        related_name="posts",
        on_delete=fields.SET_NULL,
        null=True,
        description="分类"
    )

    # 标签（多对多）
    tags = fields.ManyToManyField(
        "models.Tag",
        related_name="posts",
        through="post_tags",
        description="标签"
    )

    # 统计数据
    view_count = fields.IntField(default=0, description="浏览量")
    like_count = fields.IntField(default=0, description="点赞数")
    comment_count = fields.IntField(default=0, description="评论数")

    # 状态：draft(草稿), published(已发布), archived(已归档)
    status = fields.CharField(
        max_length=20,
        default="draft",
        description="文章状态"
    )

    # SEO
    meta_title = fields.CharField(max_length=200, null=True, description="SEO标题")
    meta_description = fields.TextField(null=True, description="SEO描述")

    # 时间戳
    published_at = fields.DatetimeField(null=True, description="发布时间")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "posts"
        ordering = ["-created_at"]
        indexes = [
            ("status", "published_at"),
            ("author", "status"),
        ]

    def __str__(self):
        return self.title


class PostTag(models.Model):
    """文章-标签关联表"""

    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    post = fields.ForeignKeyField(
        "models.Post",
        on_delete=fields.CASCADE,
        description="文章"
    )
    tag = fields.ForeignKeyField(
        "models.Tag",
        on_delete=fields.CASCADE,
        description="标签"
    )

    class Meta:
        table = "post_tags"
        unique_together = (("post", "tag"),)
