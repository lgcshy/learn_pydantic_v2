"""
Pydantic V2 学习 - 第一阶段：基础
学习时间：1小时
重点：V2 核心方法和与 V1 的区别
"""

from pydantic import BaseModel, Field
from typing import Optional

print("=" * 80)
print("第一阶段：Pydantic V2 基础")
print("=" * 80)
print()

# ===== 1. 基础模型定义 =====
print("1. 基础模型定义")
print("-" * 80)

class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None  # 可选字段
    is_active: bool = True  # 带默认值的字段

# 创建实例 - 方式1：直接传参
user1 = User(id=1, name="张三", email="zhangsan@example.com")
print(f"用户1: {user1}")
print()

# 创建实例 - 方式2：从字典创建
user_data = {
    "id": 2,
    "name": "李四",
    "email": "lisi@example.com",
    "age": 25
}
user2 = User(**user_data)
print(f"用户2: {user2}")
print()


# ===== 2. V2 核心方法（重要！）=====
print("\n2. V2 核心方法（必须掌握）")
print("-" * 80)

# 2.1 model_validate() - 从字典验证和创建
print("📌 model_validate() - 从字典创建")
data = {"id": 3, "name": "王五", "email": "wangwu@example.com"}
user3 = User.model_validate(data)
print(f"   结果: {user3}")
print()

# 2.2 model_validate_json() - 从 JSON 字符串创建
print("📌 model_validate_json() - 从 JSON 字符串创建")
json_str = '{"id": 4, "name": "赵六", "email": "zhaoliu@example.com", "age": 30}'
user4 = User.model_validate_json(json_str)
print(f"   结果: {user4}")
print()

# 2.3 model_dump() - 转换为字典
print("📌 model_dump() - 转换为字典")
user_dict = user4.model_dump()
print(f"   类型: {type(user_dict)}")
print(f"   内容: {user_dict}")
print()

# 2.4 model_dump_json() - 转换为 JSON 字符串
print("📌 model_dump_json() - 转换为 JSON 字符串")
user_json = user4.model_dump_json()
print(f"   类型: {type(user_json)}")
print(f"   内容: {user_json}")
print()

# 2.5 model_dump_json(indent=2) - 格式化的 JSON
print("📌 model_dump_json(indent=2) - 格式化输出")
user_json_pretty = user4.model_dump_json(indent=2)
print(f"   内容:\n{user_json_pretty}")
print()

# 2.6 model_copy() - 复制模型
print("📌 model_copy() - 复制模型")
user5 = user4.model_copy()
print(f"   原对象: {user4}")
print(f"   复制后: {user5}")
print(f"   是同一个对象吗？{user4 is user5}")  # False
print()

# 2.7 model_copy(update={...}) - 复制并更新
print("📌 model_copy(update={...}) - 复制并更新字段")
user6 = user4.model_copy(update={"name": "新名字", "age": 99})
print(f"   原对象: {user4}")
print(f"   更新后: {user6}")
print()


# ===== 3. V1 vs V2 对比（重要！避免混淆）=====
print("\n3. ⚠️  V1 vs V2 方法对比（必看！）")
print("-" * 80)
print("V1 方法               →  V2 方法")
print("-" * 80)
print("parse_obj()          →  model_validate()")
print("parse_raw()          →  model_validate_json()")
print("dict()               →  model_dump()")
print("json()               →  model_dump_json()")
print("copy()               →  model_copy()")
print("schema()             →  model_json_schema()")
print("parse_file()         →  已移除（手动读取文件后用 model_validate_json）")
print()


# ===== 4. 字段类型和默认值 =====
print("\n4. 字段类型和默认值")
print("-" * 80)

class Product(BaseModel):
    # 必需字段
    name: str
    price: float
    
    # 可选字段 - Optional[T] = None
    description: Optional[str] = None
    
    # 带默认值的字段
    stock: int = 0
    is_available: bool = True
    
    # 使用 Field 设置默认值和描述
    category: str = Field(default="未分类", description="产品分类")

product1 = Product(name="iPhone 15", price=5999.99)
print(f"产品1: {product1}")
print()

product2 = Product(
    name="MacBook Pro",
    price=12999.99,
    description="M3 芯片",
    stock=10,
    category="电脑"
)
print(f"产品2: {product2}")
print()


# ===== 5. 数据验证示例 =====
print("\n5. 数据验证示例")
print("-" * 80)

# 5.1 正常的数据
try:
    valid_user = User(id=100, name="正常用户", email="user@example.com")
    print(f"✅ 验证成功: {valid_user}")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

# 5.2 缺少必需字段
try:
    invalid_user = User(name="缺少ID")  # 缺少 id 和 email
    print(f"✅ 验证成功: {invalid_user}")
except Exception as e:
    print(f"❌ 验证失败: 缺少必需字段")
    print(f"   错误信息: {type(e).__name__}")
print()

# 5.3 类型错误
try:
    invalid_user = User(id="不是数字", name="张三", email="test@example.com")
    print(f"✅ 验证成功: {invalid_user}")
except Exception as e:
    print(f"❌ 验证失败: 类型错误")
    print(f"   错误信息: {type(e).__name__}")
print()


# ===== 6. 实用技巧 =====
print("\n6. 实用技巧")
print("-" * 80)

class Settings(BaseModel):
    app_name: str = "My App"
    debug: bool = False
    max_connections: int = 100

# 6.1 从环境变量或配置文件加载（模拟）
config_data = {
    "app_name": "生产环境应用",
    "debug": False,
    "max_connections": 500
}
settings = Settings.model_validate(config_data)
print(f"配置: {settings}")
print()

# 6.2 序列化控制
print("序列化控制示例:")
user = User(id=1, name="张三", email="test@example.com", age=None, is_active=True)

print(f"  完整输出: {user.model_dump()}")
print(f"  排除 None: {user.model_dump(exclude_none=True)}")
print(f"  只包含特定字段: {user.model_dump(include={'id', 'name'})}")
print(f"  排除特定字段: {user.model_dump(exclude={'email'})}")
print()


# ===== 总结 =====
print("\n" + "=" * 80)
print("第一阶段总结")
print("=" * 80)
print("""
核心要点：
1. ✅ 记住 V2 的方法都有 model_ 前缀
2. ✅ model_validate() - 从字典创建
3. ✅ model_validate_json() - 从 JSON 创建  
4. ✅ model_dump() - 转字典
5. ✅ model_dump_json() - 转 JSON
6. ✅ model_copy() - 复制实例

易错点：
❌ 不要使用 V1 的方法名（dict(), json(), parse_obj() 等）
✅ 全部改用带 model_ 前缀的新方法

下一步：学习 Field 约束和验证（02_field_constraints.py）
""")

