"""
用户 CRUD 操作
"""
from typing import Optional
from app.models.user import User
from app.core.security import get_password_hash, verify_password


class UserCRUD:
    """用户 CRUD 操作类"""

    @staticmethod
    async def get_by_id(user_id: str) -> Optional[User]:
        """根据 ID 获取用户"""
        return await User.filter(id=user_id).first()

    @staticmethod
    async def get_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return await User.filter(username=username).first()

    @staticmethod
    async def get_by_email(email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return await User.filter(email=email).first()

    @staticmethod
    async def get_by_username_or_email(username_or_email: str) -> Optional[User]:
        """根据用户名或邮箱获取用户"""
        return await User.filter(
            username=username_or_email
        ).first() or await User.filter(
            email=username_or_email
        ).first()

    @staticmethod
    async def create(username: str, email: str, password: str) -> User:
        """创建用户"""
        password_hash = get_password_hash(password)
        user = await User.create(
            username=username,
            email=email,
            password_hash=password_hash
        )
        return user

    @staticmethod
    async def update(user_id: str, **kwargs) -> Optional[User]:
        """更新用户"""
        user = await User.filter(id=user_id).first()
        if user:
            for key, value in kwargs.items():
                if value is not None and hasattr(user, key):
                    setattr(user, key, value)
            await user.save()
        return user

    @staticmethod
    async def authenticate(username_or_email: str, password: str) -> Optional[User]:
        """验证用户登录"""
        user = await UserCRUD.get_by_username_or_email(username_or_email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    async def is_superuser(user_id: str) -> bool:
        """检查用户是否为超级用户"""
        user = await User.filter(id=user_id).first()
        return user.is_superuser if user else False


user_crud = UserCRUD()
