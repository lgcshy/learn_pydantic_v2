"""
用户 SQLAlchemy 模型（数据库层）
定义数据库表结构和关系
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    """用户表模型"""

    __tablename__ = "users"

    # 主键
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # 基本信息
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # 密码（哈希后）
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # 状态标志
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # 时间戳（自动管理）
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """字符串表示，方便调试"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# 注意事项：
# 1. 使用 Mapped 和 mapped_column 是 SQLAlchemy 2.0 的推荐写法
# 2. Mapped[str | None] 表示可选字段
# 3. index=True 创建索引，提高查询性能
# 4. unique=True 确保字段值唯一
# 5. server_default 在数据库层面设置默认值
# 6. func.now() 使用数据库的时间函数

