"""
Pydantic V2 学习 - 第六阶段：别名和序列化
学习时间：1小时
重点：字段别名、序列化控制、数据导出
"""

from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Optional, List
from datetime import datetime

print("=" * 80)
print("第六阶段：别名和序列化")
print("=" * 80)
print()

# ===== 1. 基础别名 =====
print("1. 基础别名 - alias")
print("-" * 80)

class User(BaseModel):
    """用户模型 - 演示别名"""
    user_id: int = Field(alias="id")  # 输入时使用 'id'
    user_name: str = Field(alias="name")
    email_address: str = Field(alias="email")

# 创建实例 - 必须使用别名
print("使用别名创建:")
user_data = {"id": 1, "name": "张三", "email": "zhangsan@example.com"}
user = User.model_validate(user_data)
print(f"✅ {user}")
print()

# 尝试使用字段名（会失败）
print("尝试使用字段名创建:")
try:
    user2 = User(user_id=2, user_name="李四", email_address="lisi@example.com")
except Exception as e:
    print(f"❌ 失败: 必须使用别名")
print()

# 输出时使用字段名
print("序列化输出:")
print(f"  model_dump(): {user.model_dump()}")
print(f"  JSON: {user.model_dump_json()}")
print()


# ===== 2. 双向别名 - populate_by_name =====
print("\n2. 双向别名 - populate_by_name")
print("-" * 80)

class FlexibleUser(BaseModel):
    """灵活的用户模型 - 字段名和别名都可以用"""
    model_config = ConfigDict(
        populate_by_name=True  # 关键配置！
    )
    
    user_id: int = Field(alias="id")
    user_name: str = Field(alias="name")

# 使用别名
user1 = FlexibleUser(id=1, name="张三")
print(f"✅ 使用别名: {user1}")

# 使用字段名
user2 = FlexibleUser(user_id=2, user_name="李四")
print(f"✅ 使用字段名: {user2}")

# 混合使用
user3 = FlexibleUser(id=3, user_name="王五")
print(f"✅ 混合使用: {user3}")
print()


# ===== 3. 序列化别名 - serialization_alias =====
print("\n3. 序列化别名 - serialization_alias")
print("-" * 80)

class APIUser(BaseModel):
    """API 用户模型 - 输入输出使用不同名称"""
    internal_id: int = Field(
        alias="id",  # 输入时使用 'id'
        serialization_alias="userId"  # 输出时使用 'userId'
    )
    internal_name: str = Field(
        alias="name",
        serialization_alias="userName"
    )

# 创建实例
user_data = {"id": 1, "name": "张三"}
user = APIUser.model_validate(user_data)
print(f"输入数据: {user_data}")
print(f"输出数据: {user.model_dump()}")
print(f"输出 JSON: {user.model_dump_json()}")
print()

print("使用场景：")
print("  ✓ 内部使用 snake_case (internal_id)")
print("  ✓ 接收数据使用简单名 (id)")
print("  ✓ 返回数据使用 camelCase (userId)")
print()


# ===== 4. 序列化控制 =====
print("\n4. 序列化控制 - include/exclude")
print("-" * 80)

class SecureUser(BaseModel):
    """安全用户模型 - 演示序列化控制"""
    id: int
    username: str
    email: str
    password: str
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.now)

user = SecureUser(
    id=1,
    username="zhangsan",
    email="zhangsan@example.com",
    password="secret123",
    is_admin=True
)

print("完整数据:")
print(f"  {user.model_dump()}")
print()

print("排除敏感字段 (exclude):")
print(f"  {user.model_dump(exclude={'password'})}")
print()

print("只包含特定字段 (include):")
print(f"  {user.model_dump(include={'id', 'username', 'email'})}")
print()

print("排除多个字段:")
print(f"  {user.model_dump(exclude={'password', 'is_admin', 'created_at'})}")
print()


# ===== 5. 序列化过滤 =====
print("\n5. 序列化过滤")
print("-" * 80)

class OptionalUser(BaseModel):
    """演示序列化过滤"""
    id: int
    name: str
    nickname: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    is_active: bool = True

user = OptionalUser(id=1, name="张三", email="zhangsan@example.com")

print("完整数据（包含 None）:")
print(f"  {user.model_dump()}")
print()

print("排除 None 值 (exclude_none):")
print(f"  {user.model_dump(exclude_none=True)}")
print()

print("排除未设置的字段 (exclude_unset):")
print(f"  {user.model_dump(exclude_unset=True)}")
print()

print("排除默认值 (exclude_defaults):")
print(f"  {user.model_dump(exclude_defaults=True)}")
print()


# ===== 6. 自定义序列化器 =====
print("\n6. 自定义序列化器 - field_serializer")
print("-" * 80)

class Product(BaseModel):
    """产品模型 - 自定义序列化"""
    name: str
    price: float
    discount: Optional[float] = None
    
    @field_serializer('price')
    def serialize_price(self, value: float) -> str:
        """将价格格式化为货币格式"""
        return f"¥{value:.2f}"
    
    @field_serializer('discount')
    def serialize_discount(self, value: Optional[float]) -> Optional[str]:
        """将折扣转换为百分比"""
        if value is None:
            return None
        return f"{value * 100:.0f}%"

product = Product(name="iPhone 15", price=5999.99, discount=0.1)
print(f"产品对象: {product}")
print(f"序列化后: {product.model_dump()}")
print(f"JSON: {product.model_dump_json()}")
print()


# ===== 7. 嵌套模型序列化 =====
print("\n7. 嵌套模型序列化")
print("-" * 80)

class Address(BaseModel):
    street: str
    city: str
    country: str = "中国"

class Company(BaseModel):
    name: str
    address: Address

class Employee(BaseModel):
    id: int
    name: str
    company: Company
    salary: float

employee = Employee(
    id=1,
    name="张三",
    company={
        "name": "腾讯",
        "address": {"street": "科技路1号", "city": "深圳"}
    },
    salary=50000
)

print("完整序列化:")
print(employee.model_dump_json(indent=2))
print()

print("排除薪资信息:")
print(employee.model_dump(exclude={'salary'}))
print()

print("只包含公司名和城市:")
result = employee.model_dump(include={
    'company': {'name': True, 'address': {'city'}}
})
print(result)
print()


# ===== 8. 序列化模式 =====
print("\n8. 序列化模式 - mode='json'")
print("-" * 80)

from datetime import date
from uuid import UUID, uuid4

class Event(BaseModel):
    """事件模型"""
    id: UUID = Field(default_factory=uuid4)
    name: str
    event_date: date
    data: bytes = b"binary data"

event = Event(name="会议", event_date=date(2024, 1, 1))

print("Python 模式 (mode='python', 默认):")
python_dict = event.model_dump()
print(f"  id 类型: {type(python_dict['id'])}")
print(f"  event_date 类型: {type(python_dict['event_date'])}")
print(f"  data 类型: {type(python_dict['data'])}")
print()

print("JSON 模式 (mode='json'):")
json_dict = event.model_dump(mode='json')
print(f"  id 类型: {type(json_dict['id'])} - {json_dict['id']}")
print(f"  event_date 类型: {type(json_dict['event_date'])} - {json_dict['event_date']}")
print(f"  data 类型: {type(json_dict['data'])} - {json_dict['data']}")
print()


# ===== 9. by_alias 参数 =====
print("\n9. by_alias 参数")
print("-" * 80)

class APIModel(BaseModel):
    """API 模型"""
    internal_id: int = Field(alias="id")
    internal_name: str = Field(alias="name")

model = APIModel(id=1, name="测试")

print("默认输出（使用字段名）:")
print(f"  {model.model_dump()}")
print()

print("使用别名输出 (by_alias=True):")
print(f"  {model.model_dump(by_alias=True)}")
print()

print("JSON 输出（使用别名）:")
print(f"  {model.model_dump_json(by_alias=True)}")
print()


# ===== 10. 实战示例：API 响应格式化 =====
print("\n10. 实战示例：API 响应格式化")
print("-" * 80)

class UserProfile(BaseModel):
    """用户资料 - 完整的序列化控制"""
    model_config = ConfigDict(
        populate_by_name=True  # 允许字段名和别名
    )
    
    # 基本信息
    user_id: int = Field(alias="id", serialization_alias="userId")
    username: str
    email: str
    
    # 敏感信息
    password_hash: str = Field(exclude=True)  # 永远不序列化
    
    # 可选信息
    phone: Optional[str] = None
    avatar_url: Optional[str] = Field(None, serialization_alias="avatarUrl")
    
    # 管理信息
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    
    @field_serializer('created_at', 'last_login')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        """格式化时间"""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d %H:%M:%S")

# 创建用户
user = UserProfile(
    id=1,
    username="zhangsan",
    email="zhangsan@example.com",
    password_hash="hashed_password_here",
    phone="13800138000",
    is_admin=True
)

print("场景 1: 公开API响应（排除敏感信息）")
public_data = user.model_dump(
    by_alias=True,  # 使用 camelCase
    exclude_none=True,  # 排除 None
    exclude={'is_admin', 'created_at'}  # 排除管理信息
)
print(f"  {public_data}")
print()

print("场景 2: 管理后台响应（包含所有信息）")
admin_data = user.model_dump(
    by_alias=True,
    exclude_none=True
)
print(f"  {admin_data}")
print()

print("场景 3: JSON API 响应")
json_response = user.model_dump_json(
    by_alias=True,
    exclude_none=True,
    exclude={'created_at'},
    indent=2
)
print(json_response)
print()


# ===== 总结 =====
print("\n" + "=" * 80)
print("第六阶段总结")
print("=" * 80)
print("""
核心要点：
1. ✅ alias - 输入别名
2. ✅ serialization_alias - 输出别名
3. ✅ populate_by_name - 允许字段名和别名同时使用
4. ✅ include/exclude - 控制序列化字段
5. ✅ exclude_none/exclude_unset/exclude_defaults - 过滤特定值
6. ✅ by_alias - 序列化时使用别名
7. ✅ @field_serializer - 自定义序列化

序列化参数速查表：
┌────────────────────┬─────────────────────────────┐
│ 参数               │ 作用                        │
├────────────────────┼─────────────────────────────┤
│ include            │ 只包含指定字段              │
│ exclude            │ 排除指定字段                │
│ exclude_none       │ 排除值为 None 的字段        │
│ exclude_unset      │ 排除未设置的字段            │
│ exclude_defaults   │ 排除使用默认值的字段        │
│ by_alias           │ 使用别名作为键名            │
│ mode               │ 'python' 或 'json'          │
└────────────────────┴─────────────────────────────┘

别名使用场景：
• API 接口：接收 snake_case，返回 camelCase
• 数据库：字段名与表列名不同
• 向后兼容：保持旧的 API 格式

易错点：
❌ 设置别名后忘记配置 populate_by_name
❌ 混淆 alias 和 serialization_alias
✅ alias - 输入, serialization_alias - 输出

实用技巧：
• 公开 API：exclude 敏感字段 + by_alias=True
• 内部使用：include 需要的字段
• 日志记录：exclude_none=True 减少冗余

下一步：学习实战练习（07_practical.py）
""")

