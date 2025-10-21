# Pydantic V2 速查表 🚀

## V1 → V2 方法对照

| V1 方法 | V2 方法 | 说明 |
|---------|---------|------|
| `User.parse_obj(data)` | `User.model_validate(data)` | 从字典创建 |
| `User.parse_raw(json_str)` | `User.model_validate_json(json_str)` | 从 JSON 创建 |
| `user.dict()` | `user.model_dump()` | 转为字典 |
| `user.json()` | `user.model_dump_json()` | 转为 JSON |
| `user.copy()` | `user.model_copy()` | 复制模型 |
| `User.schema()` | `User.model_json_schema()` | 获取 schema |

## 核心装饰器

```python
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

# 字段验证器（单字段）
@field_validator('username')
@classmethod
def validate_username(cls, v: str) -> str:
    return v.lower()

# 模型验证器（跨字段）
@model_validator(mode='after')
def check_passwords_match(self) -> 'User':
    if self.password != self.password_confirm:
        raise ValueError('密码不一致')
    return self

# 自定义序列化
@field_serializer('price')
def serialize_price(self, value: float) -> str:
    return f"¥{value:.2f}"
```

## Field 约束

### 数值约束

```python
price: float = Field(gt=0)          # > 0 (不含)
discount: float = Field(ge=0)       # >= 0 (含)
max_price: float = Field(lt=1000)   # < 1000 (不含)
limit: float = Field(le=100)        # <= 100 (含)
```

### 字符串约束

```python
username: str = Field(min_length=3, max_length=20)
phone: str = Field(pattern=r'^1[3-9]\d{9}$')
email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
```

### 集合约束

```python
tags: List[str] = Field(min_length=1, max_length=10)
```

## 配置 ConfigDict

```python
class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,    # 去除空格
        str_min_length=1,              # 最小长度
        validate_assignment=True,      # 赋值时验证
        frozen=False,                  # True=不可变
        extra='forbid',                # 'ignore'/'allow'/'forbid'
        populate_by_name=True,         # 允许字段名+别名
        from_attributes=True,          # 从对象属性创建(原orm_mode)
        use_enum_values=False,         # 使用枚举值
        json_schema_extra={            # 额外 schema 信息
            "examples": [{"name": "张三"}]
        }
    )
```

### 常用配置组合

```python
# 严格 API 模型
model_config = ConfigDict(
    str_strip_whitespace=True,
    validate_assignment=True,
    extra='forbid'
)

# 不可变配置对象
model_config = ConfigDict(
    frozen=True,
    extra='forbid'
)

# ORM 响应模型
model_config = ConfigDict(
    from_attributes=True,
    populate_by_name=True
)
```

## 别名

```python
class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    # 输入别名
    user_id: int = Field(alias="id")
    
    # 输入+输出不同别名
    internal_id: int = Field(
        alias="id",                    # 输入用 'id'
        serialization_alias="userId"   # 输出用 'userId'
    )
```

## 序列化控制

```python
# 基础序列化
user.model_dump()                      # Python dict
user.model_dump_json()                 # JSON string
user.model_dump_json(indent=2)         # 格式化 JSON

# 字段过滤
user.model_dump(include={'id', 'name'})           # 只包含
user.model_dump(exclude={'password'})             # 排除
user.model_dump(exclude_none=True)                # 排除 None
user.model_dump(exclude_unset=True)               # 排除未设置
user.model_dump(exclude_defaults=True)            # 排除默认值

# 使用别名
user.model_dump(by_alias=True)                    # 使用别名作为键

# 嵌套包含/排除
user.model_dump(include={
    'company': {'name', 'address': {'city'}}
})
```

## 类型提示

```python
from typing import List, Dict, Set, Tuple, Optional, Union

tags: List[str]                        # 列表
scores: Dict[str, int]                 # 字典
unique_ids: Set[int]                   # 集合（去重）
point: Tuple[float, float]             # 固定长度元组
nickname: Optional[str] = None         # 可选
contact: Union[str, int]               # 多种类型之一
```

## 可变默认值

```python
# ❌ 错误
tags: List[str] = []
scores: Dict[str, int] = {}

# ✅ 正确
tags: List[str] = Field(default_factory=list)
scores: Dict[str, int] = Field(default_factory=dict)
metadata: Dict = Field(default_factory=lambda: {"v": "1.0"})
```

## 验证器模式

```python
# mode='before' - 原始数据预处理
@model_validator(mode='before')
@classmethod
def preprocess(cls, data: dict) -> dict:
    # 接收原始字典，在类型转换前
    return data

# mode='after' - 模型实例验证（最常用）
@model_validator(mode='after')
def validate(self) -> 'User':
    # 接收模型实例，在类型转换后
    return self
```

## 快速示例

### 基础模型

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    is_active: bool = True

# 创建
user = User(id=1, name="张三", email="test@example.com")
user = User.model_validate({"id": 1, "name": "张三", "email": "test@example.com"})

# 序列化
user.model_dump()          # dict
user.model_dump_json()     # JSON string
```

### 验证模型

```python
class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    password_confirm: str
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('只能包含字母和数字')
        return v.lower()
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegister':
        if self.password != self.password_confirm:
            raise ValueError('密码不一致')
        return self
```

### 嵌套模型

```python
class Address(BaseModel):
    street: str
    city: str

class Person(BaseModel):
    name: str
    address: Address
    emails: List[str]

person = Person(
    name="张三",
    address={"street": "中关村", "city": "北京"},
    emails=["test@example.com"]
)
```

## 常见错误

| ❌ 错误 | ✅ 正确 |
|---------|---------|
| `user.dict()` | `user.model_dump()` |
| `Field("value")` | `Field(default="value")` |
| `@validator` | `@field_validator` + `@classmethod` |
| `tags: List = []` | `Field(default_factory=list)` |
| `class Config:` | `model_config = ConfigDict()` |
| `orm_mode = True` | `from_attributes = True` |
| 验证器忘记 `return` | 必须返回值 |
| `Optional[str]` 无默认值 | `Optional[str] = None` |

## 记忆口诀

```
V2 方法 model_ 前缀不能忘
验证器要 classmethod 和 return 值
可变默认 default_factory 来帮忙
gt/lt 不包含 ge/le 要包含
```

---

**快速查询完毕！祝编码愉快！** 🎉

