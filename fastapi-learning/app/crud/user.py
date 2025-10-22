"""
用户 CRUD 操作
继承基类并添加用户特定的方法
"""
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """用户 CRUD 操作类"""

    def get_by_email(self, db: Session, *, email: str) -> User | None:
        """
        根据邮箱获取用户
        Args:
            db: 数据库会话
            email: 用户邮箱
        Returns:
            用户对象或 None
        """
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()

    def get_by_username(self, db: Session, *, username: str) -> User | None:
        """
        根据用户名获取用户
        Args:
            db: 数据库会话
            username: 用户名
        Returns:
            用户对象或 None
        """
        stmt = select(User).where(User.username == username)
        return db.execute(stmt).scalar_one_or_none()

    def get_by_username_or_email(
        self, db: Session, *, identifier: str
    ) -> User | None:
        """
        根据用户名或邮箱获取用户（用于登录）
        Args:
            db: 数据库会话
            identifier: 用户名或邮箱
        Returns:
            用户对象或 None
        """
        stmt = select(User).where(
            or_(User.username == identifier, User.email == identifier)
        )
        return db.execute(stmt).scalar_one_or_none()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        创建用户（重写以处理密码哈希）
        Args:
            db: 数据库会话
            obj_in: 用户创建 Schema
        Returns:
            创建的用户对象
        """
        # 创建用户对象，但用哈希密码替换明文密码
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True,
            is_superuser=False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate | dict
    ) -> User:
        """
        更新用户（重写以处理密码哈希）
        Args:
            db: 数据库会话
            db_obj: 要更新的用户对象
            obj_in: 更新 Schema 或字典
        Returns:
            更新后的用户对象
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # 如果更新密码，需要哈希处理
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> User | None:
        """
        验证用户（登录）
        Args:
            db: 数据库会话
            username: 用户名或邮箱
            password: 密码
        Returns:
            用户对象（验证成功）或 None（验证失败）
        """
        user = self.get_by_username_or_email(db, identifier=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """检查用户是否激活"""
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """检查用户是否是超级用户"""
        return user.is_superuser

    def create_superuser(
        self, db: Session, *, email: str, username: str, password: str
    ) -> User:
        """
        创建超级用户
        Args:
            db: 数据库会话
            email: 邮箱
            username: 用户名
            password: 密码
        Returns:
            创建的超级用户对象
        """
        db_obj = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password),
            is_active=True,
            is_superuser=True,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# 创建全局 CRUD 实例
user_crud = CRUDUser(User)


# CRUD 设计最佳实践：
# 1. 继承通用基类避免重复代码
# 2. 添加模型特定的查询方法（如 get_by_email）
# 3. 重写方法以处理特殊逻辑（如密码哈希）
# 4. 提供认证等业务逻辑方法
# 5. 创建全局实例方便使用

