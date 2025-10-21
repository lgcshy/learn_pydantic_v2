"""
Pydantic V2 学习 - 第五阶段：Model Config 配置
学习时间：1小时
重点：掌握 ConfigDict，控制模型行为
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

print("=" * 80)
print("第五阶段：Model Config 配置")
print("=" * 80)
print()

# ===== 1. V2 配置语法（重要变化）=====
print("1. V2 配置语法")
print("-" * 80)

print("⚠️  V1 vs V2 配置语法对比:")
print("""
V1 (已过时):
class User(BaseModel):
    class Config:
        str_strip_whitespace = True
        validate_assignment = True

V2 (新语法):
from pydantic import ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )
""")
print()


# ===== 2. 字符串处理配置 =====
print("\n2. 字符串处理配置")
print("-" * 80)

class User(BaseModel):
    """演示字符串处理配置"""
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自动去除首尾空格
        str_min_length=1,  # 字符串最小长度（去除空格后）
        str_max_length=100  # 字符串最大长度
    )
    
    username: str
    email: str

# 测试
user = User(username="  zhangsan  ", email="  test@example.com  ")
print(f"✅ 创建用户:")
print(f"   username: '{user.username}' (空格已去除)")
print(f"   email: '{user.email}' (空格已去除)")
print()


# ===== 3. 验证配置 =====
print("\n3. 验证配置")
print("-" * 80)

class Product1(BaseModel):
    """默认行为：创建后可以修改，但不验证"""
    name: str
    price: float = Field(gt=0)

product1 = Product1(name="测试", price=100)
print(f"product1 初始价格: {product1.price}")
product1.price = -50  # 不会报错！
print(f"product1 修改后价格: {product1.price} (负数！没有验证)")
print()

class Product2(BaseModel):
    """启用赋值验证"""
    model_config = ConfigDict(
        validate_assignment=True  # 赋值时也进行验证
    )
    
    name: str
    price: float = Field(gt=0)

product2 = Product2(name="测试", price=100)
print(f"product2 初始价格: {product2.price}")
try:
    product2.price = -50  # 会报错！
except Exception as e:
    print(f"❌ 修改失败（正确的！）: 价格不能为负数")
print()


# ===== 4. 不可变模型 =====
print("\n4. 不可变模型 (Frozen)")
print("-" * 80)

class ImmutableUser(BaseModel):
    """不可变用户模型"""
    model_config = ConfigDict(
        frozen=True  # 模型不可变
    )
    
    id: int
    username: str

user = ImmutableUser(id=1, username="zhangsan")
print(f"创建用户: {user}")

try:
    user.username = "lisi"  # 尝试修改
except Exception as e:
    print(f"❌ 修改失败（正确的！）: 模型是不可变的")
print()

print("使用场景：")
print("  ✓ 配置对象（不应该被修改）")
print("  ✓ 值对象（Value Object）")
print("  ✓ 需要作为字典键的对象")
print()


# ===== 5. 别名配置 =====
print("\n5. 别名配置")
print("-" * 80)

class UserWithAlias(BaseModel):
    """演示别名配置"""
    model_config = ConfigDict(
        populate_by_name=True  # 允许使用字段名或别名
    )
    
    user_id: int = Field(alias="id")
    user_name: str = Field(alias="name")

# 测试
print("测试 1: 使用别名创建")
user1 = UserWithAlias(id=1, name="张三")
print(f"✅ {user1}")
print()

print("测试 2: 使用字段名创建（需要 populate_by_name=True）")
user2 = UserWithAlias(user_id=2, user_name="李四")
print(f"✅ {user2}")
print()

print("测试 3: 混合使用")
user3 = UserWithAlias(id=3, user_name="王五")
print(f"✅ {user3}")
print()


# ===== 6. 额外字段处理 =====
print("\n6. 额外字段处理")
print("-" * 80)

class StrictModel(BaseModel):
    """严格模式：不允许额外字段"""
    model_config = ConfigDict(
        extra='forbid'  # 禁止额外字段
    )
    
    name: str
    age: int

print("strict='forbid' - 禁止额外字段:")
try:
    user = StrictModel(name="张三", age=25, unknown_field="值")
except Exception as e:
    print(f"❌ 创建失败（正确的！）: 不允许额外字段 'unknown_field'")
print()

class IgnoreModel(BaseModel):
    """忽略模式：忽略额外字段（默认行为）"""
    model_config = ConfigDict(
        extra='ignore'  # 忽略额外字段（默认）
    )
    
    name: str
    age: int

print("extra='ignore' - 忽略额外字段（默认）:")
user = IgnoreModel(name="李四", age=30, unknown_field="会被忽略")
print(f"✅ 创建成功: {user}")
print(f"   unknown_field 被忽略了")
print()

class AllowModel(BaseModel):
    """允许模式：保留额外字段"""
    model_config = ConfigDict(
        extra='allow'  # 允许并保留额外字段
    )
    
    name: str
    age: int

print("extra='allow' - 允许额外字段:")
user = AllowModel(name="王五", age=35, city="北京", hobby="编程")
print(f"✅ 创建成功: {user}")
print(f"   完整数据: {user.model_dump()}")
print()


# ===== 7. ORM 模式（重要！）=====
print("\n7. ORM 模式配置")
print("-" * 80)

# 模拟 ORM 对象
class ORMUser:
    """模拟数据库 ORM 对象"""
    def __init__(self):
        self.id = 1
        self.username = "zhangsan"
        self.email = "zhangsan@example.com"
        self.is_active = True

class UserSchema(BaseModel):
    """从 ORM 对象创建的 Pydantic 模型"""
    model_config = ConfigDict(
        from_attributes=True  # V2: 允许从对象属性创建（V1 中叫 orm_mode）
    )
    
    id: int
    username: str
    email: str
    is_active: bool

# 从 ORM 对象创建
orm_user = ORMUser()
pydantic_user = UserSchema.model_validate(orm_user)
print(f"✅ 从 ORM 对象创建:")
print(f"   {pydantic_user}")
print()

print("使用场景：")
print("  ✓ 与 SQLAlchemy 等 ORM 集成")
print("  ✓ 从数据库查询结果创建 Pydantic 模型")
print("  ✓ FastAPI 返回 ORM 对象时自动序列化")
print()


# ===== 8. JSON Schema 配置 =====
print("\n8. JSON Schema 配置")
print("-" * 80)

class APIModel(BaseModel):
    """API 模型 - 带 JSON Schema 配置"""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "zhangsan",
                    "email": "zhangsan@example.com",
                    "age": 25
                }
            ],
            "description": "用户信息模型"
        }
    )
    
    username: str = Field(description="用户名")
    email: str = Field(description="邮箱地址")
    age: int = Field(description="年龄", ge=0, le=150)

# 获取 JSON Schema
schema = APIModel.model_json_schema()
print("JSON Schema:")
print(f"  Title: {schema.get('title')}")
print(f"  Description: {schema.get('description')}")
print(f"  Examples: {schema.get('examples')}")
print()


# ===== 9. 常用配置组合 =====
print("\n9. 常用配置组合")
print("-" * 80)

print("配置 1: 严格的 API 模型")
print("-" * 40)
print("""
class StrictAPIModel(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 去除空格
        validate_assignment=True,   # 赋值验证
        extra='forbid',             # 禁止额外字段
        frozen=False                # 可修改
    )
""")
print()

print("配置 2: 不可变配置对象")
print("-" * 40)
print("""
class Config(BaseModel):
    model_config = ConfigDict(
        frozen=True,                # 不可变
        validate_assignment=True,   # 赋值验证（虽然不可变）
        extra='forbid'              # 禁止额外字段
    )
""")
print()

print("配置 3: ORM 响应模型")
print("-" * 40)
print("""
class ORMResponseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,       # 从 ORM 创建
        str_strip_whitespace=True,  # 去除空格
        validate_assignment=False,  # 不需要赋值验证
        extra='ignore'              # 忽略额外字段
    )
""")
print()

print("配置 4: 宽松的内部模型")
print("-" * 40)
print("""
class InternalModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',              # 允许额外字段
        validate_assignment=False,  # 不验证赋值
        str_strip_whitespace=False  # 不处理空格
    )
""")
print()


# ===== 10. 配置参数完整列表 =====
print("\n10. 配置参数完整列表")
print("-" * 80)
print("""
常用配置参数：

字符串处理：
  • str_strip_whitespace: bool - 去除字符串首尾空格
  • str_to_lower: bool - 转换为小写
  • str_to_upper: bool - 转换为大写
  • str_min_length: int - 最小长度
  • str_max_length: int - 最大长度

验证：
  • validate_assignment: bool - 赋值时验证
  • validate_default: bool - 验证默认值
  • validate_return: bool - 验证返回值

行为：
  • frozen: bool - 模型不可变
  • extra: str - 额外字段处理 ('forbid', 'ignore', 'allow')
  • populate_by_name: bool - 允许使用字段名和别名

ORM/对象：
  • from_attributes: bool - 从对象属性创建（原 orm_mode）

JSON Schema：
  • json_schema_extra: dict - 额外的 JSON Schema 信息
  • title: str - 模型标题
  • use_enum_values: bool - 使用枚举值而不是枚举对象

其他：
  • arbitrary_types_allowed: bool - 允许任意类型
  • ser_json_timedelta: str - timedelta 序列化方式
  • ser_json_bytes: str - bytes 序列化方式
""")


# ===== 总结 =====
print("\n" + "=" * 80)
print("第五阶段总结")
print("=" * 80)
print("""
核心要点：
1. ✅ V2 使用 model_config = ConfigDict(...) 配置
2. ✅ str_strip_whitespace - 自动去除空格（常用）
3. ✅ validate_assignment - 赋值时验证（推荐）
4. ✅ frozen - 不可变模型
5. ✅ extra - 控制额外字段（forbid/ignore/allow）
6. ✅ from_attributes - 从 ORM 对象创建（重要）
7. ✅ populate_by_name - 允许字段名和别名同时使用

V1 vs V2 对比：
┌──────────────────┬──────────────────────┐
│ V1 配置          │ V2 配置              │
├──────────────────┼──────────────────────┤
│ class Config:    │ model_config =       │
│     orm_mode     │     from_attributes  │
└──────────────────┴──────────────────────┘

易错点：
❌ 使用 V1 的 class Config 语法
✅ 使用 V2 的 model_config = ConfigDict(...)

❌ orm_mode (V1)
✅ from_attributes (V2)

实用技巧：
• API 模型：str_strip_whitespace=True, validate_assignment=True
• 配置类：frozen=True
• ORM 模型：from_attributes=True

下一步：学习别名和序列化（06_aliases_serialization.py）
""")

