"""
Pydantic V2 学习 - 第八阶段：常见错误对比
学习时间：30分钟
重点：避免常见陷阱，掌握正确写法
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import List, Optional

print("=" * 80)
print("第八阶段：常见错误对比")
print("=" * 80)
print()

# ===== 错误 1: 使用 V1 方法名 =====
print("错误 1: 使用 V1 方法名")
print("=" * 80)

print("❌ 错误示例 (V1 写法):")
print("""
class User(BaseModel):
    name: str

# V1 方法（在 V2 中不存在）
User.parse_obj({"name": "张三"})  # AttributeError
user.dict()  # AttributeError
user.json()  # AttributeError
""")
print()

print("✅ 正确写法 (V2):")
print("""
class User(BaseModel):
    name: str

# V2 方法
User.model_validate({"name": "张三"})
user.model_dump()
user.model_dump_json()
""")
print()

class User(BaseModel):
    name: str

user = User.model_validate({"name": "张三"})
print(f"正确结果: {user}")
print()


# ===== 错误 2: Field 参数不使用关键字 =====
print("\n错误 2: Field 参数不使用关键字")
print("=" * 80)

print("❌ 错误示例:")
print("""
class Product(BaseModel):
    name: str = Field("默认名称", min_length=1)  # 错误！
    price: float = Field(0, gt=0)  # 错误！
""")
print()

print("✅ 正确写法:")
print("""
class Product(BaseModel):
    name: str = Field(default="默认名称", min_length=1)
    price: float = Field(default=0, gt=0)
""")
print()

class Product(BaseModel):
    name: str = Field(default="默认名称", min_length=1)
    price: float = Field(default=0, gt=0)

product = Product()
print(f"正确结果: {product}")
print()


# ===== 错误 3: 使用 @validator 而不是 @field_validator =====
print("\n错误 3: 使用 V1 的 @validator")
print("=" * 80)

print("❌ 错误示例 (V1):")
print("""
from pydantic import validator  # V1

class User(BaseModel):
    username: str
    
    @validator('username')  # V1 装饰器
    def check_username(cls, v):
        return v.lower()
""")
print()

print("✅ 正确写法 (V2):")
print("""
from pydantic import field_validator  # V2

class User(BaseModel):
    username: str
    
    @field_validator('username')
    @classmethod
    def check_username(cls, v: str) -> str:
        return v.lower()
""")
print()

class UserCorrect(BaseModel):
    username: str
    
    @field_validator('username')
    @classmethod
    def check_username(cls, v: str) -> str:
        return v.lower()

user = UserCorrect(username="ZHANGSAN")
print(f"正确结果: {user.username}")
print()


# ===== 错误 4: 验证器忘记 @classmethod =====
print("\n错误 4: 验证器忘记 @classmethod")
print("=" * 80)

print("❌ 错误示例:")
print("""
class User(BaseModel):
    name: str
    
    @field_validator('name')
    def validate_name(cls, v):  # 缺少 @classmethod
        return v.strip()
    
# 运行时会报错！
""")
print()

print("✅ 正确写法:")
print("""
class User(BaseModel):
    name: str
    
    @field_validator('name')
    @classmethod  # 必须添加！
    def validate_name(cls, v: str) -> str:
        return v.strip()
""")
print()


# ===== 错误 5: 验证器忘记返回值 =====
print("\n错误 5: 验证器忘记返回值")
print("=" * 80)

print("❌ 错误示例:")
print("""
class User(BaseModel):
    age: int
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int):
        if v < 18:
            raise ValueError('年龄必须>=18')
        # 忘记 return v ！
    
# 结果：age 会变成 None
""")
print()

print("✅ 正确写法:")
print("""
class User(BaseModel):
    age: int
    
    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError('年龄必须>=18')
        return v  # 必须返回！
""")
print()


# ===== 错误 6: 可变默认值 =====
print("\n错误 6: 使用可变默认值")
print("=" * 80)

print("❌ 错误示例:")
print("""
class User(BaseModel):
    tags: List[str] = []  # 危险！所有实例共享同一个列表
    scores: Dict[str, int] = {}  # 危险！

# 问题：
user1 = User()
user2 = User()
user1.tags.append("tag1")
# user2.tags 也会包含 "tag1"！
""")
print()

print("✅ 正确写法:")
print("""
from pydantic import Field

class User(BaseModel):
    tags: List[str] = Field(default_factory=list)
    scores: Dict[str, int] = Field(default_factory=dict)
    
# 现在每个实例都有独立的列表和字典
""")
print()

class UserCorrect2(BaseModel):
    tags: List[str] = Field(default_factory=list)

user1 = UserCorrect2()
user2 = UserCorrect2()
user1.tags.append("tag1")
print(f"user1.tags: {user1.tags}")  # ['tag1']
print(f"user2.tags: {user2.tags}")  # []
print("✅ 每个实例独立")
print()


# ===== 错误 7: 使用 V1 的 Config 语法 =====
print("\n错误 7: 使用 V1 的 Config 语法")
print("=" * 80)

print("❌ 错误示例 (V1):")
print("""
class User(BaseModel):
    class Config:  # V1 语法
        str_strip_whitespace = True
        validate_assignment = True
        orm_mode = True
""")
print()

print("✅ 正确写法 (V2):")
print("""
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        from_attributes=True  # V2 中改名了
    )
""")
print()


# ===== 错误 8: 混淆 gt/ge, lt/le =====
print("\n错误 8: 混淆 gt/ge, lt/le")
print("=" * 80)

print("❌ 常见误解:")
print("""
class Product(BaseModel):
    price: float = Field(gt=0)  # price > 0 (不包含0)
    
# price=0 会报错！
Product(price=0)  # ValidationError
""")
print()

print("✅ 正确理解:")
print("""
gt (greater than)       > 0   不包含0
ge (greater or equal)   >= 0  包含0
lt (less than)          < 10  不包含10
le (less or equal)      <= 10 包含10

# 如果要允许0，使用 ge
class Product(BaseModel):
    discount: float = Field(ge=0)  # >= 0, 可以等于0
""")
print()


# ===== 错误 9: 别名配置不完整 =====
print("\n错误 9: 别名配置不完整")
print("=" * 80)

print("❌ 错误示例:")
print("""
class User(BaseModel):
    user_id: int = Field(alias="id")

# 尝试使用字段名
User(user_id=1)  # ValidationError!
# 必须使用别名
User(id=1)  # OK
""")
print()

print("✅ 正确写法（如果想两者都能用）:")
print("""
class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True  # 允许字段名和别名
    )
    user_id: int = Field(alias="id")

# 现在两种都可以
User(id=1)  # OK
User(user_id=1)  # 也 OK
""")
print()


# ===== 错误 10: 混淆 alias 和 serialization_alias =====
print("\n错误 10: 混淆 alias 和 serialization_alias")
print("=" * 80)

print("概念区分:")
print("""
alias:               输入别名（创建实例时使用）
serialization_alias: 输出别名（序列化时使用）
""")
print()

print("❌ 错误理解:")
print("""
class User(BaseModel):
    internal_id: int = Field(alias="id")

user = User(id=1)
print(user.model_dump())
# 输出: {'internal_id': 1}  # 使用字段名，不是别名！
""")
print()

print("✅ 正确使用:")
print("""
class User(BaseModel):
    internal_id: int = Field(
        alias="id",              # 输入时用 'id'
        serialization_alias="userId"  # 输出时用 'userId'
    )

user = User(id=1)
print(user.model_dump())         # {'internal_id': 1}
print(user.model_dump(by_alias=True))  # {'userId': 1}
""")
print()

class UserCorrect3(BaseModel):
    internal_id: int = Field(
        alias="id",
        serialization_alias="userId"
    )

user = UserCorrect3(id=1)
print(f"默认输出: {user.model_dump()}")
print(f"使用别名: {user.model_dump(by_alias=True)}")
print()


# ===== 错误 11: Optional 类型误用 =====
print("\n错误 11: Optional 类型误用")
print("=" * 80)

print("❌ 错误理解:")
print("""
class User(BaseModel):
    name: Optional[str]  # 没有默认值
    
# 这个字段仍然是必需的！
User()  # ValidationError: Field required
""")
print()

print("✅ 正确理解:")
print("""
# 可选字段 = Optional + 默认值
class User(BaseModel):
    # 方式1: Optional + None
    name: Optional[str] = None
    
    # 方式2: 使用 Field
    age: Optional[int] = Field(None)
    
    # 方式3: 使用 | 语法 (Python 3.10+)
    # nickname: str | None = None

# 现在字段是真正可选的
User()  # OK
""")
print()


# ===== 错误 12: model_validator 的 mode 混淆 =====
print("\n错误 12: model_validator 的 mode 混淆")
print("=" * 80)

print("mode='before' vs mode='after':")
print("""
mode='before':
  • 接收原始输入数据（dict）
  • 在类型转换之前执行
  • 需要 @classmethod
  • 用于预处理数据

mode='after':
  • 接收模型实例（self）
  • 在类型转换之后执行
  • 不需要 @classmethod
  • 用于跨字段验证（最常用）
""")
print()

print("❌ 错误示例:")
print("""
class User(BaseModel):
    password: str
    password_confirm: str
    
    @model_validator(mode='before')  # 错误的 mode
    def check_passwords(self):  # before 需要 @classmethod
        if self.password != self.password_confirm:  # self 不存在！
            raise ValueError('密码不一致')
        return self
""")
print()

print("✅ 正确写法:")
print("""
class User(BaseModel):
    password: str
    password_confirm: str
    
    @model_validator(mode='after')  # 正确的 mode
    def check_passwords(self) -> 'User':
        if self.password != self.password_confirm:
            raise ValueError('密码不一致')
        return self
""")
print()


# ===== 错误汇总 =====
print("\n" + "=" * 80)
print("常见错误汇总")
print("=" * 80)
print("""
┌────┬─────────────────────────┬──────────────────────────────┐
│ #  │ 错误                    │ 正确做法                     │
├────┼─────────────────────────┼──────────────────────────────┤
│ 1  │ user.dict()             │ user.model_dump()            │
│ 2  │ User.parse_obj()        │ User.model_validate()        │
│ 3  │ Field("value")          │ Field(default="value")       │
│ 4  │ @validator              │ @field_validator             │
│ 5  │ 忘记 @classmethod       │ 总是添加 @classmethod        │
│ 6  │ 忘记 return v           │ 验证器必须返回值             │
│ 7  │ tags: List[str] = []    │ Field(default_factory=list)  │
│ 8  │ class Config:           │ model_config = ConfigDict()  │
│ 9  │ orm_mode = True         │ from_attributes = True       │
│ 10 │ gt=0 允许0              │ gt>0不含, ge>=0含           │
│ 11 │ 别名但未配置 by_name    │ populate_by_name=True        │
│ 12 │ Optional[str] 无默认值  │ Optional[str] = None         │
└────┴─────────────────────────┴──────────────────────────────┘

记忆技巧：
• V2 方法都有 model_ 前缀
• 验证器需要 @classmethod 和 return
• 可变类型用 default_factory
• Config 改用 ConfigDict
• gt/lt 不含边界，ge/le 含边界

下一步：查看完整学习指南（README_LEARNING.md）
""")

