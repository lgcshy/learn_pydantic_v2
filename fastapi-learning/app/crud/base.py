"""
通用 CRUD 基类
提供基本的增删改查操作，避免重复代码
"""
from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base

# 类型变量
ModelType = TypeVar("ModelType", bound=Base)  # SQLAlchemy 模型
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # 创建 Schema
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # 更新 Schema


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """通用 CRUD 操作基类"""

    def __init__(self, model: type[ModelType]):
        """
        初始化 CRUD 对象
        Args:
            model: SQLAlchemy 模型类
        """
        self.model = model

    def get(self, db: Session, id: int) -> ModelType | None:
        """
        根据 ID 获取单个对象
        Args:
            db: 数据库会话
            id: 对象 ID
        Returns:
            模型对象或 None
        """
        return db.get(self.model, id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """
        获取多个对象（分页）
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
        Returns:
            对象列表
        """
        stmt = select(self.model).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def get_count(self, db: Session) -> int:
        """
        获取总数
        Args:
            db: 数据库会话
        Returns:
            记录总数
        """
        stmt = select(self.model)
        return len(db.execute(stmt).scalars().all())

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建新对象
        Args:
            db: 数据库会话
            obj_in: 创建 Schema 对象
        Returns:
            创建的模型对象
        """
        # 将 Pydantic 模型转换为字典
        obj_in_data = obj_in.model_dump()
        # 创建 SQLAlchemy 模型实例
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)  # 刷新以获取数据库生成的字段（如 ID）
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """
        更新对象
        Args:
            db: 数据库会话
            db_obj: 要更新的数据库对象
            obj_in: 更新 Schema 对象或字典
        Returns:
            更新后的模型对象
        """
        # 获取当前对象的数据
        obj_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}

        # 获取更新数据
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)  # 只更新提供的字段

        # 应用更新
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType | None:
        """
        删除对象
        Args:
            db: 数据库会话
            id: 对象 ID
        Returns:
            删除的对象或 None
        """
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# CRUD 基类使用说明：
# 1. 使用泛型支持类型提示
# 2. 所有方法都返回类型化的对象
# 3. exclude_unset=True 确保只更新提供的字段
# 4. 使用 SQLAlchemy 2.0 的 select() API
# 5. commit() 后使用 refresh() 获取最新数据

