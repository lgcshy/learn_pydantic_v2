"""
数据库连接和会话管理
支持同步 SQLAlchemy 操作（学习阶段使用同步更简单）
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# 创建数据库引擎
# connect_args 仅用于 SQLite，其他数据库可以移除
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG,  # 在调试模式下打印 SQL 语句
    pool_pre_ping=True,  # 连接池预检查，确保连接有效
)

# 创建会话工厂
# autocommit=False: 需要显式提交事务
# autoflush=False: 需要显式刷新到数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# SQLAlchemy 2.0 风格的声明式基类
class Base(DeclarativeBase):
    """所有模型的基类"""

    pass


# 数据库会话依赖（用于依赖注入）
def get_db():
    """
    获取数据库会话的依赖函数
    使用 yield 确保会话在请求结束后关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 初始化数据库
def init_db() -> None:
    """创建所有表（仅用于开发/学习，生产环境应使用 Alembic）"""
    # 导入所有模型以确保它们被注册
    from app.models import user  # noqa: F401

    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功")


# 删除所有表（仅用于测试）
def drop_db() -> None:
    """删除所有表（谨慎使用！）"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️  数据库表已删除")


if __name__ == "__main__":
    # 测试数据库连接
    print(f"数据库 URL: {settings.DATABASE_URL}")
    print(f"数据库引擎: {engine}")

    # 测试创建会话
    db = SessionLocal()
    print(f"会话创建成功: {db}")
    db.close()
    print("✅ 数据库连接测试成功")

