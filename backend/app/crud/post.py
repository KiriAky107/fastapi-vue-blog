"""
文章 CRUD 操作
"""
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from app.models.post import Post, PostTag
from app.models.user import User
from app.models.category import Category
from app.models.tag import Tag
from app.core.database import with_transaction


class PostCRUD:
    """文章 CRUD 操作类"""

    @staticmethod
    async def get_by_id(post_id: str) -> Optional[Post]:
        """根据 ID 获取文章"""
        return await Post.filter(id=post_id).first()

    @staticmethod
    async def get_by_slug(slug: str) -> Optional[Post]:
        """根据 slug 获取文章"""
        return await Post.filter(slug=slug).first()

    @staticmethod
    async def get_all(
        page: int = 1,
        page_size: int = 10,
        status: str = "published",
        category_id: Optional[str] = None,
        tag_id: Optional[str] = None
    ) -> Tuple[List[Post], int]:
        """获取文章列表（分页）"""
        query = Post.all()

        if status:
            query = query.filter(status=status)

        if category_id:
            query = query.filter(category_id=category_id)

        if tag_id:
            query = query.filter(tags__id=tag_id)

        total = await query.count()
        posts = await query \
            .prefetch_related("author", "category", "tags") \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .order_by("-created_at")

        return posts, total

    @staticmethod
    async def get_by_author(
        author_id: str,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Post], int]:
        """获取指定作者的文章列表"""
        query = Post.filter(author_id=author_id)
        total = await query.count()
        posts = await query \
            .prefetch_related("author", "category", "tags") \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .order_by("-created_at")
        return posts, total

    @staticmethod
    async def create(
        title: str,
        slug: str,
        content: str,
        author_id: str,
        summary: Optional[str] = None,
        cover_image: Optional[str] = None,
        category_id: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
        status: str = "draft",
        meta_title: Optional[str] = None,
        meta_description: Optional[str] = None
    ) -> Post:
        """创建文章（带事务）"""
        async with with_transaction():
            post = await Post.create(
                title=title,
                slug=slug,
                content=content,
                author_id=author_id,
                summary=summary,
                cover_image=cover_image,
                category_id=category_id,
                status=status,
                meta_title=meta_title,
                meta_description=meta_description
            )

            # 添加标签
            if tag_ids:
                for tag_id in tag_ids:
                    await PostTag.create(post_id=post.id, tag_id=tag_id)

            return post

    @staticmethod
    async def update(post_id: str, **kwargs) -> Optional[Post]:
        """更新文章（带事务）"""
        post = await Post.filter(id=post_id).first()
        if not post:
            return None

        async with with_transaction():
            # 处理标签更新
            if "tag_ids" in kwargs:
                tag_ids = kwargs.pop("tag_ids")
                # 删除旧标签关联
                await PostTag.filter(post_id=post_id).delete()
                # 添加新标签关联
                for tag_id in tag_ids:
                    await PostTag.create(post_id=post_id, tag_id=tag_id)

            # 处理发布状态更新
            if kwargs.get("status") == "published" and not post.published_at:
                kwargs["published_at"] = datetime.now(timezone.utc)

            for key, value in kwargs.items():
                if value is not None and hasattr(post, key):
                    setattr(post, key, value)

            await post.save()
            return post

    @staticmethod
    async def delete(post_id: str) -> bool:
        """删除文章"""
        post = await Post.filter(id=post_id).first()
        if post:
            await post.delete()
            return True
        return False

    @staticmethod
    async def increment_view_count(post_id: str) -> None:
        """增加浏览量"""
        await Post.filter(id=post_id).update(view_count=Post.view_count + 1)

    @staticmethod
    async def increment_like_count(post_id: str) -> None:
        """增加点赞数"""
        await Post.filter(id=post_id).update(like_count=Post.like_count + 1)

    @staticmethod
    async def get_hot_posts(limit: int = 10) -> List[Post]:
        """获取热门文章（按浏览量排序）"""
        return await Post.filter(status="published") \
            .prefetch_related("author", "category") \
            .order_by("-view_count") \
            .limit(limit)

    @staticmethod
    async def get_recent_posts(limit: int = 10) -> List[Post]:
        """获取最新文章"""
        return await Post.filter(status="published") \
            .prefetch_related("author", "category", "tags") \
            .order_by("-created_at") \
            .limit(limit)

    @staticmethod
    async def search(
        query: str,
        page: int = 1,
        page_size: int = 10
    ) -> Tuple[List[Post], int]:
        """搜索文章"""
        from tortoise.query_utils import Q

        q = Q(title__icontains=query) | Q(content__icontains=query) | Q(summary__icontains=query)

        posts_query = Post.filter(q, status="published")
        total = await posts_query.count()
        posts = await posts_query \
            .prefetch_related("author", "category", "tags") \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .order_by("-created_at")

        return posts, total


post_crud = PostCRUD()
