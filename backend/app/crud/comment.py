"""
评论 CRUD 操作
"""
from typing import Optional, List, Tuple
from app.models.comment import Comment
from app.models.post import Post


class CommentCRUD:
    """评论 CRUD 操作类"""

    @staticmethod
    async def get_by_id(comment_id: str) -> Optional[Comment]:
        """根据 ID 获取评论"""
        return await Comment.filter(id=comment_id).first()

    @staticmethod
    async def get_by_post(
        post_id: str,
        page: int = 1,
        page_size: int = 20,
        approved_only: bool = True
    ) -> Tuple[List[Comment], int]:
        """获取文章的所有评论（树形结构）"""
        query = Comment.filter(post_id=post_id)

        if approved_only:
            query = query.filter(is_approved=True)

        total = await query.count()
        comments = await query \
            .prefetch_related("author", "replies__author") \
            .filter(parent_id=None) \
            .offset((page - 1) * page_size) \
            .limit(page_size) \
            .order_by("created_at")

        return comments, total

    @staticmethod
    async def create(
        content: str,
        author_id: str,
        post_id: str,
        parent_id: Optional[str] = None,
        is_approved: bool = True
    ) -> Comment:
        """创建评论"""
        comment = await Comment.create(
            content=content,
            author_id=author_id,
            post_id=post_id,
            parent_id=parent_id,
            is_approved=is_approved
        )

        # 更新文章的评论数
        await Post.filter(id=post_id).update(comment_count=Post.comment_count + 1)

        return comment

    @staticmethod
    async def update(comment_id: str, **kwargs) -> Optional[Comment]:
        """更新评论"""
        comment = await Comment.filter(id=comment_id).first()
        if comment:
            for key, value in kwargs.items():
                if value is not None and hasattr(comment, key):
                    setattr(comment, key, value)
            await comment.save()
        return comment

    @staticmethod
    async def delete(comment_id: str) -> bool:
        """删除评论"""
        comment = await Comment.filter(id=comment_id).first()
        if comment:
            post_id = comment.post_id
            await comment.delete()
            # 更新文章的评论数
            await Post.filter(id=post_id).update(comment_count=Post.comment_count - 1)
            return True
        return False

    @staticmethod
    async def approve(comment_id: str) -> Optional[Comment]:
        """审核通过评论"""
        return await CommentCRUD.update(comment_id, is_approved=True)


comment_crud = CommentCRUD()
