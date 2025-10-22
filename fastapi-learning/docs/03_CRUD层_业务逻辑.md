# CRUD 层 - 业务逻辑深入解析

## 🎯 什么是 CRUD？

**CRUD** = **C**reate, **R**ead, **U**pdate, **D**elete

CRUD 层的职责：

- 封装所有数据库操作
- 处理业务逻辑
- 提供统一的接口
- 与 API 层解耦

## 📐 通用 CRUD 基类设计

### 为什么需要基类？

```python
# ❌ 没有基类 - 每个模型都要重复写
class UserCRUD:
    def get(self, db, id):
        ...
    def get_multi(self, db, skip, limit):
        ...
    def create(self, db, obj_in):
        ...

class PostCRUD:
    def get(self, db, id):
        ...  # 重复代码
    def get_multi(self, db, skip, limit):
        ...  # 重复代码
    def create(self, db, obj_in):
        ...  # 重复代码

# ✅ 有基类 - 继承即可
class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    pass  # 自动获得所有基础方法

class PostCRUD(CRUDBase[Post, PostCreate, PostUpdate]):
    pass  # 自动获得所有基础方法
```

### 泛型基类实现

```python
from typing import Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import Base

# 类型变量
ModelType = TypeVar("ModelType", bound=Base)  # SQLAlchemy 模型
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # 创建 Schema
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # 更新 Schema

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """通用 CRUD 操作基类"""
    
    def __init__(self, model: type[ModelType]):
        self.model = model
```

**泛型的好处：**

- 类型安全
- IDE 自动补全
- 可以针对不同模型定制

## 🔍 Read 操作详解

### 1. 获取单个对象

```python
def get(self, db: Session, id: int) -> ModelType | None:
    """根据 ID 获取对象"""
    return db.get(self.model, id)  # SQLAlchemy 2.0 推荐方式
```

**使用：**

```python
user = user_crud.get(db, id=1)
if user is None:
    raise HTTPException(status_code=404, detail="用户不存在")
```

### 2. 获取多个对象（分页）

```python
def get_multi(
    self, 
    db: Session, 
    *, 
    skip: int = 0, 
    limit: int = 100
) -> list[ModelType]:
    """获取多个对象（分页）"""
    stmt = select(self.model).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())
```

**使用：**

```python
# 获取第1页，每页10条
users = user_crud.get_multi(db, skip=0, limit=10)

# 获取第2页
users = user_crud.get_multi(db, skip=10, limit=10)

# 页码转换
page = 2
page_size = 10
skip = (page - 1) * page_size
users = user_crud.get_multi(db, skip=skip, limit=page_size)
```

### 3. 获取总数

```python
def get_count(self, db: Session) -> int:
    """获取总数"""
    stmt = select(self.model)
    return len(db.execute(stmt).scalars().all())
```

**更高效的方式：**

```python
from sqlalchemy import func, select

def get_count(self, db: Session) -> int:
    """获取总数"""
    stmt = select(func.count()).select_from(self.model)
    return db.execute(stmt).scalar()
```

## ➕ Create 操作详解

```python
def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
    """创建新对象"""
    # 1. Pydantic Schema → 字典
    obj_in_data = obj_in.model_dump()
    
    # 2. 字典 → SQLAlchemy 模型
    db_obj = self.model(**obj_in_data)
    
    # 3. 添加到会话
    db.add(db_obj)
    
    # 4. 提交事务
    db.commit()
    
    # 5. 刷新对象（获取数据库生成的字段，如 ID）
    db.refresh(db_obj)
    
    return db_obj
```

**为什么需要 refresh？**

```python
# 创建前
user = User(username="john", email="john@example.com")
print(user.id)  # None
print(user.created_at)  # None

db.add(user)
db.commit()

# 提交后但未刷新
print(user.id)  # None（本地对象还没更新）

db.refresh(user)

# 刷新后
print(user.id)  # 1（从数据库获取）
print(user.created_at)  # 2024-01-01 12:00:00
```

## 🔄 Update 操作详解

```python
def update(
    self,
    db: Session,
    *,
    db_obj: ModelType,
    obj_in: UpdateSchemaType | dict[str, Any],
) -> ModelType:
    """更新对象"""
    # 获取当前对象的数据
    obj_data = {c.name: getattr(db_obj, c.name) for c in db_obj.__table__.columns}
    
    # 获取更新数据
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        # exclude_unset=True：只更新提供的字段
        update_data = obj_in.model_dump(exclude_unset=True)
    
    # 应用更新
    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
```

**exclude_unset 的重要性：**

```python
# 假设数据库中的用户
user = User(id=1, username="john", email="john@example.com", full_name="John Doe")

# 用户只想更新邮箱
update_data = UserUpdate(email="newemail@example.com")

# ❌ 不使用 exclude_unset
data = update_data.model_dump()
# {'email': 'newemail@example.com', 'username': None, 'full_name': None}
# 会把其他字段设为 None！

# ✅ 使用 exclude_unset
data = update_data.model_dump(exclude_unset=True)
# {'email': 'newemail@example.com'}
# 只更新提供的字段
```

## ❌ Delete 操作详解

```python
def delete(self, db: Session, *, id: int) -> ModelType | None:
    """删除对象"""
    obj = db.get(self.model, id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
```

**软删除实现：**

```python
# 模型添加 is_deleted 字段
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

# CRUD 方法
def soft_delete(self, db: Session, *, id: int) -> ModelType | None:
    """软删除（标记为已删除）"""
    obj = db.get(self.model, id)
    if obj:
        obj.is_deleted = True
        db.commit()
        db.refresh(obj)
    return obj

def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
    """获取未删除的对象"""
    stmt = select(self.model).where(self.model.is_deleted == False)
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())
```

## 🎯 特定模型的 CRUD 扩展

### 用户 CRUD 示例

```python
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """用户 CRUD 操作"""
    
    # 自定义查询方法
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        """根据邮箱获取用户"""
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalar_one_or_none()
    
    def get_by_username(self, db: Session, *, username: str) -> User | None:
        """根据用户名获取用户"""
        stmt = select(User).where(User.username == username)
        return db.execute(stmt).scalar_one_or_none()
    
    # 重写 create 方法（处理密码哈希）
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建用户（密码哈希）"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),  # 哈希密码
            is_active=True,
            is_superuser=False,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    # 业务逻辑方法
    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> User | None:
        """验证用户（登录）"""
        user = self.get_by_username_or_email(db, identifier=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
```

## 🔍 高级查询

### 1. 过滤查询

```python
def get_active_users(self, db: Session) -> list[User]:
    """获取活跃用户"""
    stmt = select(User).where(User.is_active == True)
    return list(db.execute(stmt).scalars().all())

def search_by_username(self, db: Session, *, keyword: str) -> list[User]:
    """搜索用户名"""
    stmt = select(User).where(User.username.contains(keyword))
    return list(db.execute(stmt).scalars().all())
```

### 2. 排序

```python
def get_multi_sorted(
    self, db: Session, *, skip: int = 0, limit: int = 100
) -> list[User]:
    """获取用户列表（按创建时间倒序）"""
    stmt = select(User).order_by(User.created_at.desc())
    stmt = stmt.offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())
```

### 3. 联合查询（Join）

```python
def get_users_with_posts(self, db: Session) -> list[User]:
    """获取有文章的用户"""
    stmt = (
        select(User)
        .join(Post)
        .where(Post.is_published == True)
        .distinct()
    )
    return list(db.execute(stmt).scalars().all())
```

## 🛡️ 事务处理

### 手动事务控制

```python
def create_user_with_profile(
    self, db: Session, *, user_in: UserCreate, profile_in: ProfileCreate
) -> User:
    """创建用户和资料（事务）"""
    try:
        # 创建用户
        user = User(**user_in.model_dump())
        db.add(user)
        db.flush()  # 刷新以获取 user.id，但不提交
        
        # 创建资料
        profile = Profile(**profile_in.model_dump(), user_id=user.id)
        db.add(profile)
        
        # 一起提交
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()  # 回滚
        raise
```

## 🎯 最佳实践

1. **使用泛型基类**
   - 避免重复代码
   - 提高类型安全性

2. **继承并扩展**
   - 继承基类获得通用方法
   - 添加模型特定的方法

3. **业务逻辑放在 CRUD 层**
   - 不要在 API 层处理业务逻辑
   - CRUD 层负责数据验证和转换

4. **使用 exclude_unset**
   - 更新时只修改提供的字段
   - 避免覆盖其他字段

5. **错误处理**
   - CRUD 方法返回 None 而不是抛出异常
   - 让 API 层决定如何处理

6. **创建全局实例**

   ```python
   user_crud = CRUDUser(User)
   ```

## 📊 完整示例：文章 CRUD

```python
# models/post.py
class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)

# crud/post.py
class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Post]:
        """获取用户的文章"""
        stmt = select(Post).where(Post.user_id == user_id)
        stmt = stmt.offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())
    
    def get_published(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[Post]:
        """获取已发布的文章"""
        stmt = select(Post).where(Post.is_published == True)
        stmt = stmt.order_by(Post.created_at.desc())
        stmt = stmt.offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

post_crud = CRUDPost(Post)
```

## 📚 参考资料

- [SQLAlchemy Select API](https://docs.sqlalchemy.org/en/20/core/selectable.html)
- [SQLAlchemy ORM 查询](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)
- [Python 泛型](https://docs.python.org/3/library/typing.html#generics)
- [SQLAlchemy soft delete](https://pypi.org/project/sqlalchemy-easy-softdelete/)

