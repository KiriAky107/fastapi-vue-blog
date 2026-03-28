"""
分类 CRUD 操作
"""
from typing import Optional, List
from app.models.category import Category


class CategoryCRUD:
    """分类 CRUD 操作类"""

    @staticmethod
    async def get_by_id(category_id: str) -> Optional[Category]:
        """根据 ID 获取分类"""
        return await Category.filter(id=category_id).first()

    @staticmethod
    async def get_by_slug(slug: str) -> Optional[Category]:
        """根据 slug 获取分类"""
        return await Category.filter(slug=slug).first()

    @staticmethod
    async def get_all() -> List[Category]:
        """获取所有分类"""
        return await Category.all()

    @staticmethod
    async def create(name: str, slug: str, description: Optional[str] = None) -> Category:
        """创建分类"""
        category = await Category.create(
            name=name,
            slug=slug,
            description=description
        )
        return category

    @staticmethod
    async def update(category_id: str, **kwargs) -> Optional[Category]:
        """更新分类"""
        category = await Category.filter(id=category_id).first()
        if category:
            for key, value in kwargs.items():
                if value is not None and hasattr(category, key):
                    setattr(category, key, value)
            await category.save()
        return category

    @staticmethod
    async def delete(category_id: str) -> bool:
        """删除分类"""
        category = await Category.filter(id=category_id).first()
        if category:
            await category.delete()
            return True
        return False

    @staticmethod
    async def get_with_post_count() -> List[dict]:
        """获取分类及其文章数量"""
        categories = await Category.all().prefetch_related("posts")
        result = []
        for cat in categories:
            result.append({
                "id": str(cat.id),
                "name": cat.name,
                "slug": cat.slug,
                "description": cat.description,
                "post_count": len(cat.posts) if cat.posts else 0
            })
        return result


category_crud = CategoryCRUD()
