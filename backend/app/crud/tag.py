"""
标签 CRUD 操作
"""
from typing import Optional, List
from app.models.tag import Tag


class TagCRUD:
    """标签 CRUD 操作类"""

    @staticmethod
    async def get_by_id(tag_id: str) -> Optional[Tag]:
        """根据 ID 获取标签"""
        return await Tag.filter(id=tag_id).first()

    @staticmethod
    async def get_by_slug(slug: str) -> Optional[Tag]:
        """根据 slug 获取标签"""
        return await Tag.filter(slug=slug).first()

    @staticmethod
    async def get_by_name(name: str) -> Optional[Tag]:
        """根据名称获取标签"""
        return await Tag.filter(name=name).first()

    @staticmethod
    async def get_all() -> List[Tag]:
        """获取所有标签"""
        return await Tag.all()

    @staticmethod
    async def create(name: str, slug: str) -> Tag:
        """创建标签"""
        tag = await Tag.create(name=name, slug=slug)
        return tag

    @staticmethod
    async def update(tag_id: str, **kwargs) -> Optional[Tag]:
        """更新标签"""
        tag = await Tag.filter(id=tag_id).first()
        if tag:
            for key, value in kwargs.items():
                if value is not None and hasattr(tag, key):
                    setattr(tag, key, value)
            await tag.save()
        return tag

    @staticmethod
    async def delete(tag_id: str) -> bool:
        """删除标签"""
        tag = await Tag.filter(id=tag_id).first()
        if tag:
            await tag.delete()
            return True
        return False

    @staticmethod
    async def get_or_create(name: str, slug: str) -> Tag:
        """获取或创建标签"""
        tag = await TagCRUD.get_by_slug(slug)
        if tag:
            return tag
        return await TagCRUD.create(name, slug)


tag_crud = TagCRUD()
