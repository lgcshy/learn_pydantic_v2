# Models 层 - SQLAlchemy 深入解析

## 📚 什么是 ORM？

**ORM (Object-Relational Mapping)** - 对象关系映射

- 将数据库表映射为 Python 类
- 将表的行映射为对象实例
- 将列映射为对象属性

**好处：**

- 使用 Python 代码操作数据库
- 不需要写原始 SQL
- 数据库无关（可以轻松切换数据库）
- 类型安全

## 🔧 SQLAlchemy 2.0 新特性

### 类型化的列定义

```python
# ❌ 旧方式 (SQLAlchemy 1.x)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)

# ✅ 新方式 (SQLAlchemy 2.0)
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
```

**优势：**

- IDE 可以提供类型提示
- 更明确的类型信息
- 更好的代码自动补全

### Mapped 类型详解

```python
# 必需字段
email: Mapped[str] = mapped_column(String)

# 可选字段（可以为 NULL）
full_name: Mapped[str | None] = mapped_column(String, nullable=True)

# 带默认值的字段
is_active: Mapped[bool] = mapped_column(Boolean, default=True)
```

## 📝 用户模型详解

```python
class User(Base):
    """用户表模型"""
    
    __tablename__ = "users"  # 表名
    
    # 主键
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,  # 设为主键
        index=True,        # 创建索引
    )
    
    # 唯一字段
    email: Mapped[str] = mapped_column(
        String(255),       # 最大长度 255
        unique=True,       # 唯一约束
        index=True,        # 创建索引（加速查询）
        nullable=False,    # 不能为 NULL
    )
    
    # 可选字段
    full_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,     # 可以为 NULL
    )
    
    # 时间戳（自动管理）
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # 数据库级别的默认值
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # 更新时自动更新
        nullable=False,
    )
```

## 🔗 字段类型对照表

| Python 类型 | SQLAlchemy 类型 | 数据库类型 (SQLite) | 数据库类型 (PostgreSQL) |
|------------|----------------|-------------------|----------------------|
| `int` | `Integer` | `INTEGER` | `INTEGER` |
| `str` | `String(n)` | `VARCHAR(n)` | `VARCHAR(n)` |
| `bool` | `Boolean` | `BOOLEAN` | `BOOLEAN` |
| `float` | `Float` | `REAL` | `REAL` |
| `datetime` | `DateTime` | `TIMESTAMP` | `TIMESTAMP` |
| `date` | `Date` | `DATE` | `DATE` |
| `Decimal` | `Numeric` | `NUMERIC` | `NUMERIC` |

## 🎯 常用参数详解

### primary_key

```python
id: Mapped[int] = mapped_column(Integer, primary_key=True)
```

- 设置为主键
- 自动递增（对于 Integer 类型）
- 唯一且不能为 NULL

### unique

```python
email: Mapped[str] = mapped_column(String, unique=True)
```

- 确保值唯一
- 数据库会创建唯一约束
- 尝试插入重复值会报错

### index

```python
username: Mapped[str] = mapped_column(String, index=True)
```

- 创建数据库索引
- 加速基于该字段的查询
- 占用额外存储空间

### nullable

```python
# 必需字段
email: Mapped[str] = mapped_column(String, nullable=False)

# 可选字段
full_name: Mapped[str | None] = mapped_column(String, nullable=True)
```

- `nullable=False`：字段不能为 NULL
- `nullable=True`：字段可以为 NULL

### default vs server_default

```python
# Python 级别的默认值
is_active: Mapped[bool] = mapped_column(Boolean, default=True)

# 数据库级别的默认值
created_at: Mapped[datetime] = mapped_column(
    DateTime, server_default=func.now()
)
```

**区别：**

- `default`：在 Python 代码中设置默认值
- `server_default`：在数据库中设置默认值（更可靠）

## 🔍 时间戳最佳实践

```python
from datetime import datetime
from sqlalchemy import DateTime, func

class User(Base):
    # 创建时间（自动设置，不可修改）
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),  # 使用时区
        server_default=func.now(),  # 数据库函数
        nullable=False,
    )
    
    # 更新时间（自动设置，自动更新）
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # 更新时自动更新
        nullable=False,
    )
```

**为什么使用 `func.now()`？**

- 使用数据库的时间函数
- 确保时间一致性
- 避免客户端时间不准确

## 🎨 模型关系（预告）

### 一对多关系

```python
# 用户（一方）
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")

# 文章（多方）
class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship("User", back_populates="posts")
```

### 多对多关系

```python
# 关联表
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id")),
    Column("tag_id", ForeignKey("tags.id")),
)

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=post_tags)

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    posts: Mapped[list["Post"]] = relationship("Post", secondary=post_tags)
```

## 🛠️ 调试技巧

### __repr__ 方法

```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
```

使用场景：

```python
user = db.query(User).first()
print(user)  # <User(id=1, username='john')>
```

## 📊 数据库迁移（Alembic）

**开发环境：** 可以使用 `Base.metadata.create_all()`

**生产环境：** 应该使用 Alembic 管理迁移

```bash
# 初始化 Alembic
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "Add users table"

# 应用迁移
alembic upgrade head
```

## 🎯 练习

1. 创建 `Post` 模型（文章表）
2. 创建 `Comment` 模型（评论表）
3. 创建 `Tag` 模型（标签表）
4. 建立模型之间的关系

## 📚 参考资料

- [SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/en/20/)
- [Mapped 和 mapped_column](https://docs.sqlalchemy.org/en/20/orm/mapping_api.html)
- [Column 类型](https://docs.sqlalchemy.org/en/20/core/types.html)

