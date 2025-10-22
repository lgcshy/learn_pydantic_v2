# Schemas 层 - Pydantic V2 深入解析

## 🎯 为什么需要 Schemas？

**问题：** 为什么不直接使用 SQLAlchemy Models？

```python
# ❌ 不好的做法
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user  # 直接返回数据库对象
```

**问题：**

1. 会暴露敏感信息（如 `hashed_password`）
2. 无法控制响应格式
3. 创建和更新的字段需求不同
4. 无法添加计算字段

**解决方案：** 使用 Pydantic Schemas

## 📐 Schema 设计模式

### 基础继承结构

```python
# 1. 基础 Schema（共享字段）
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str | None = None

# 2. 创建 Schema（输入，所有字段必填）
class UserCreate(UserBase):
    password: str

# 3. 更新 Schema（输入，所有字段可选）
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = None

# 4. 响应 Schema（输出，包含数据库生成的字段）
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, dt: datetime, _info) -> str:
        """将 datetime 序列化为指定格式：YYYY-MM-DD HH:MM:SS"""
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    model_config = ConfigDict(from_attributes=True)

# 5. 内部 Schema（包含敏感信息，仅内部使用）
class UserInDB(UserBase):
    id: int
    hashed_password: str
    
    model_config = ConfigDict(from_attributes=True)
```

### 为什么这样设计？

| Schema 类型 | 用途 | 特点 |
|------------|------|------|
| `UserBase` | 共享字段 | 避免重复定义 |
| `UserCreate` | 创建用户 | 包含密码，所有字段必填 |
| `UserUpdate` | 更新用户 | 所有字段可选 |
| `UserResponse` | API 响应 | 不包含密码，包含 ID |
| `UserInDB` | 内部使用 | 包含哈希密码 |

## 🔧 Pydantic V2 核心特性

### 1. model_config (替代 Config 类)

```python
# ❌ Pydantic V1
class UserResponse(BaseModel):
    id: int
    email: str
    
    class Config:
        orm_mode = True

# ✅ Pydantic V2
class UserResponse(BaseModel):
    id: int
    email: str
    
    model_config = ConfigDict(from_attributes=True)
```

### 2. Field 验证和文档

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr = Field(
        ...,  # 必需字段
        description="用户邮箱",
        examples=["user@example.com"],
    )
    
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9_]+$",  # 正则验证
        description="用户名（只能包含字母、数字和下划线）",
        examples=["johndoe"],
    )
    
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="密码（至少8位）",
        examples=["SecurePass123"],
    )
    
    age: int | None = Field(
        None,  # 可选，默认为 None
        ge=0,  # 大于等于 0
        le=150,  # 小于等于 150
        description="年龄",
    )
```

### 3. 字段验证器

```python
from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    username: str
    password: str
    password_confirm: str
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """验证用户名只包含字母数字"""
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """验证密码强度"""
        if len(v) < 8:
            raise ValueError('密码至少8位')
        if not any(c.isupper() for c in v):
            raise ValueError('密码必须包含大写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v
```

### 4. 模型验证器（跨字段验证）

```python
from pydantic import BaseModel, model_validator

class UserCreate(BaseModel):
    password: str
    password_confirm: str
    
    @model_validator(mode='after')
    def passwords_match(self):
        """验证两次密码是否一致"""
        if self.password != self.password_confirm:
            raise ValueError('两次密码不一致')
        return self
```

### 5. 计算字段

```python
from pydantic import BaseModel, computed_field

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    
    @computed_field
    @property
    def full_name(self) -> str:
        """计算字段：全名"""
        return f"{self.first_name} {self.last_name}"
    
    model_config = ConfigDict(from_attributes=True)
```

## 🎨 常用字段类型

### 基础类型

```python
from pydantic import BaseModel

class Example(BaseModel):
    # 字符串
    name: str
    
    # 整数
    age: int
    
    # 浮点数
    price: float
    
    # 布尔值
    is_active: bool
    
    # 可选字段
    nickname: str | None = None
    
    # 带默认值
    role: str = "user"
```

### 特殊类型

```python
from pydantic import BaseModel, EmailStr, HttpUrl, UUID4, constr
from datetime import datetime, date

class Example(BaseModel):
    # 邮箱（自动验证格式）
    email: EmailStr
    
    # URL（自动验证格式）
    website: HttpUrl
    
    # UUID
    id: UUID4
    
    # 约束字符串
    username: constr(min_length=3, max_length=50)
    
    # 日期时间
    created_at: datetime
    
    # 日期
    birthday: date
```

### 集合类型

```python
from pydantic import BaseModel

class Example(BaseModel):
    # 列表
    tags: list[str]
    
    # 字典
    metadata: dict[str, Any]
    
    # 集合
    permissions: set[str]
    
    # 元组
    coordinates: tuple[float, float]
```

## 📊 Schema 序列化

### model_dump() - 转换为字典

```python
# ❌ Pydantic V1
user_dict = user.dict()

# ✅ Pydantic V2
user_dict = user.model_dump()

# 排除某些字段
user_dict = user.model_dump(exclude={'password'})

# 只包含某些字段
user_dict = user.model_dump(include={'id', 'username'})

# 排除未设置的字段（用于更新）
user_dict = user.model_dump(exclude_unset=True)
```

### model_dump_json() - 转换为 JSON

```python
# 转换为 JSON 字符串
user_json = user.model_dump_json()

# 格式化输出
user_json = user.model_dump_json(indent=2)
```

### model_validate() - 从对象创建

```python
# ❌ Pydantic V1
user_schema = UserResponse.from_orm(user_db)

# ✅ Pydantic V2
user_schema = UserResponse.model_validate(user_db)
```

## 🎯 实战示例

### 分页响应 Schema

```python
from pydantic import BaseModel, Field
from typing import Generic, TypeVar

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """通用分页响应"""
    total: int = Field(..., description="总数")
    items: list[T] = Field(..., description="数据列表")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    
    @computed_field
    @property
    def total_pages(self) -> int:
        """总页数"""
        return (self.total + self.page_size - 1) // self.page_size

# 使用
class UserListResponse(PaginatedResponse[UserResponse]):
    pass
```

### 嵌套 Schema

```python
class AddressSchema(BaseModel):
    street: str
    city: str
    country: str

class UserResponse(BaseModel):
    id: int
    username: str
    # 嵌套对象
    address: AddressSchema | None = None
    
    model_config = ConfigDict(from_attributes=True)
```

### JSON Schema 示例

```python
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePass123",
            }
        }
    )
```

这会在 Swagger UI 中显示示例。

## ⚡ 性能优化

### 1. 使用 exclude_unset

```python
# 更新时只发送修改的字段
@app.put("/users/{user_id}")
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = user_crud.get(db, id=user_id)
    # 只更新提供的字段
    update_data = user_in.model_dump(exclude_unset=True)
    user = user_crud.update(db, db_obj=user, obj_in=update_data)
    return user
```

### 2. 响应模型优化

```python
# 列表响应时排除不必要的字段
class UserListItem(BaseModel):
    id: int
    username: str
    # 不包含创建时间等详细信息
    
    model_config = ConfigDict(from_attributes=True)

@app.get("/users/", response_model=list[UserListItem])
def get_users(db: Session = Depends(get_db)):
    return user_crud.get_multi(db)
```

## 🎓 最佳实践

1. **分离不同用途的 Schema**
   - Create: 创建时的输入
   - Update: 更新时的输入（字段可选）
   - Response: 返回给客户端（不含敏感信息）

2. **使用继承避免重复**
   - 提取共享字段到 Base Schema

3. **添加详细的文档**
   - 使用 `Field(description=...)` 添加描述
   - 使用 `json_schema_extra` 添加示例

4. **验证业务规则**
   - 使用 `field_validator` 验证单个字段
   - 使用 `model_validator` 验证多字段关系

5. **永不返回敏感信息**
   - 密码字段永远不要出现在响应 Schema 中

## 📚 参考资料

- [Pydantic V2 文档](https://docs.pydantic.dev/latest/)
- [Field 类型](https://docs.pydantic.dev/latest/concepts/fields/)
- [验证器](https://docs.pydantic.dev/latest/concepts/validators/)

