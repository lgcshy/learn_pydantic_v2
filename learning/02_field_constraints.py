"""
Pydantic V2 学习 - 第二阶段：Field 约束和验证
学习时间：1.5小时
重点：掌握各种字段约束，防止无效数据
"""

from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from typing import Optional
from datetime import datetime

print("=" * 80)
print("第二阶段：Field 约束和验证")
print("=" * 80)
print()

# ===== 1. 数值约束 =====
print("1. 数值约束")
print("-" * 80)

class Product(BaseModel):
    """产品模型 - 演示数值约束"""
    name: str
    price: float = Field(gt=0, description="价格必须大于0")  # gt: greater than
    discount_price: float = Field(ge=0, description="折扣价大于等于0")  # ge: greater or equal
    stock: int = Field(ge=0, le=10000, description="库存 0-10000")  # le: less or equal
    rating: float = Field(ge=0.0, le=5.0, description="评分 0-5")

# 测试正常数据
try:
    product = Product(
        name="iPhone 15",
        price=5999.99,
        discount_price=5499.00,
        stock=100,
        rating=4.8
    )
    print(f"✅ 创建成功: {product}")
    product1 = Product(
        name="Vivo X100",
        price=4999.99,
        discount_price=4499.00,
        stock=50,
        rating=4.7
    )
    print(f"✅ 创建成功: {product1}")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

# 测试边界值
print("测试边界值:")
try:
    # price=0 会失败，因为 gt=0（必须大于0）
    invalid_product = Product(name="测试", price=0, discount_price=0, stock=0, rating=0)
except Exception as e:
    print(f"❌ 验证失败: {e}")
    print(f"❌ price=0 失败（正确的！因为 gt=0）")
print()

try:
    # discount_price=0 可以，因为 ge=0（大于等于0）
    valid_product = Product(name="测试", price=0.01, discount_price=0, stock=0, rating=0)
    print(f"✅ discount_price=0 成功（因为 ge=0）")
except Exception as e:
    print(f"❌ 失败: {e}")
print()


# ===== 2. 字符串约束 =====
print("\n2. 字符串约束")
print("-" * 80)

class User(BaseModel):
    """用户模型 - 演示字符串约束"""
    username: str = Field(min_length=3, max_length=20, description="用户名3-20字符")
    password: str = Field(min_length=8, description="密码至少8字符")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介最多500字符")
    
    # 正则表达式约束
    phone: Optional[str] = Field(
        None,
        pattern=r'^1[3-9]\d{9}$',
        description="中国手机号"
    )

# 测试
try:
    user = User(
        username="zhangsan",
        password="secure123456",
        bio="这是一段个人简介",
        phone="13800138000"
    )
    print(f"✅ 创建成功: {user}")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

# 测试失败情况
print("测试约束:")
try:
    # 用户名太短
    user = User(username="ab", password="12345678")
except Exception as e:
    print(f"❌ 用户名太短（ab < 3个字符）")
print()

try:
    # 密码太短
    user = User(username="test123", password="1234567")
except Exception as e:
    print(f"❌ 密码太短（1234567 < 8个字符）")
print()

try:
    # 手机号格式错误
    user = User(username="test123", password="12345678", phone="12345")
except Exception as e:
    print(f"❌ 手机号格式错误（不匹配正则表达式）")
print()


# ===== 3. 特殊类型约束 =====
print("\n3. 特殊类型约束")
print("-" * 80)
print("注意：EmailStr 和 HttpUrl 需要安装额外依赖：")
print("pip install pydantic[email]")
print()

class ContactInfo(BaseModel):
    """联系信息 - 演示特殊类型"""
    name: str
    email: EmailStr  # 需要: pip install pydantic[email]
    website: HttpUrl  # 自动验证 URL 格式
    
    # 替代方案：使用正则表达式
    email: str = Field(pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    website: str = Field(pattern=r'^https?://.+')

try:
    contact = ContactInfo(
        name="张三",
        email="zhangsan@example.com",
        website="https://example.com"
    )
    print(f"✅ 创建成功: {contact}")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

try:
    # 邮箱格式错误
    contact1 = ContactInfo(
        name="李四",
        email="lisi@example",
        website="https://example.com"
    )
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

try:
    # 网站格式错误
    contact2 = ContactInfo(
        name="王五",
        email="wangwu@example.com",
        website="abc"
    )
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

# ===== 4. 集合约束 =====
print("\n4. 集合约束")
print("-" * 80)

from typing import List, Set

class Article(BaseModel):
    """文章模型 - 演示集合约束"""
    title: str = Field(min_length=1, max_length=200)
    tags: List[str] = Field(min_length=1, max_length=10, description="1-10个标签")
    unique_tags: Set[str] = Field(description="自动去重的标签")

try:
    article = Article(
        title="Pydantic V2 教程",
        tags=["Python", "Pydantic", "教程"],
        unique_tags={"Python", "Pydantic", "Python"}  # 会自动去重
    )
    print(f"✅ 创建成功: {article}")
    print(f"   tags: {article.tags}")
    print(f"   unique_tags: {article.unique_tags}")  # Python 只出现一次
    # 打印unique_tags的类型
    print(f"   unique_tags 类型: {type(article.unique_tags)}")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()


# ===== 5. Field 参数完整示例 =====
print("\n5. Field 参数完整示例")
print("-" * 80)

class CompleteExample(BaseModel):
    """展示 Field 的各种参数"""
    
    # 必需字段（使用 ... 表示）
    required_field: str = Field(..., description="必需字段")
    
    # 带默认值
    optional_field: str = Field(default="默认值", description="可选字段")
    
    # 数值约束
    score: int = Field(default=0, ge=0, le=100, description="分数 0-100")
    
    # 字符串约束  
    code: str = Field(min_length=6, max_length=6, pattern=r'^\d{6}$', description="6位数字验证码")
    
    # 示例值（用于文档）
    name: str = Field(examples=["张三", "李四"])
    
    # 别名（后面章节详细讲）
    internal_id: int = Field(alias="id", description="使用 id 作为输入别名")

# 使用示例
try:
    example = CompleteExample(
        required_field="必需的",
        code="123456",
        name="王五",
        id=100  # 使用别名 id，实际存储在 internal_id
    )
    print(f"✅ 创建成功:")
    print(f"   {example}")
    print(f"   internal_id: {example.internal_id}")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()


# ===== 6. 易错点演示 =====
print("\n6. ⚠️  常见易错点")
print("-" * 80)

print("易错点 1: Field 参数必须使用关键字参数")
print("-" * 40)

# ❌ 错误写法
try:
    class WrongModel1(BaseModel):
        # name: str = Field("default_name", min_length=1)  # 错误！
        pass
    print("这个写法会报错")
except Exception as e:
    print(f"错误: {e}")

# ✅ 正确写法
class CorrectModel1(BaseModel):
    name: str = Field(default="default_name", min_length=1)

print("✅ 正确: Field(default='default_name', min_length=1)")
print()


print("易错点 2: 必需字段使用 ... 而不是 default")
print("-" * 40)

class ExampleModel(BaseModel):
    # 必需字段 - 方式1（简洁）
    field1: str
    
    # 必需字段 - 方式2（需要添加元数据时）
    field2: str = Field(..., description="必需字段")
    
    # 可选字段
    field3: str = Field(default="默认值")
    field4: Optional[str] = None

print("✅ 必需字段: Field(...)  或  field: type")
print("✅ 可选字段: Field(default=...) 或 Optional[T] = None")
print()


print("易错点 3: gt vs ge, lt vs le 的区别")
print("-" * 40)

class ComparisonModel(BaseModel):
    price_gt: float = Field(gt=0)      # > 0, 不包含0
    price_ge: float = Field(ge=0)      # >= 0, 包含0
    discount_lt: float = Field(lt=1)   # < 1, 不包含1
    discount_le: float = Field(le=1)   # <= 1, 包含1

print("gt (greater than)       : >  不包含边界值")
print("ge (greater or equal)   : >= 包含边界值")
print("lt (less than)          : <  不包含边界值")
print("le (less or equal)      : <= 包含边界值")
print()


# ===== 7. 实战练习 =====
print("\n7. 实战练习：创建用户注册表单验证")
print("-" * 80)

class UserRegistration(BaseModel):
    """用户注册表单"""
    username: str = Field(
        min_length=3,
        max_length=20,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="用户名：3-20个字符，只能包含字母、数字、下划线"
    )
    
    password: str = Field(
        min_length=8,
        max_length=50,
        description="密码：至少8个字符"
    )
    
    email: str = Field(
        pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        description="邮箱地址"
    )
    
    age: int = Field(
        ge=18,
        le=150,
        description="年龄：18-150岁"
    )
    
    phone: Optional[str] = Field(
        None,
        pattern=r'^1[3-9]\d{9}$',
        description="手机号（可选）"
    )

# 测试数据
test_cases = [
    {
        "name": "正常注册",
        "data": {
            "username": "zhangsan_123",
            "password": "securePass123",
            "email": "zhangsan@example.com",
            "age": 25,
            "phone": "13800138000"
        }
    },
    {
        "name": "用户名太短",
        "data": {
            "username": "ab",
            "password": "12345678",
            "email": "test@example.com",
            "age": 25
        }
    },
    {
        "name": "年龄不够",
        "data": {
            "username": "test123",
            "password": "12345678",
            "email": "test@example.com",
            "age": 17
        }
    }
]

for test in test_cases:
    try:
        user = UserRegistration.model_validate(test["data"])
        print(f"✅ {test['name']}: 验证通过")
    except Exception as e:
        print(f"❌ {test['name']}: 验证失败")
print()


# ===== 总结 =====
print("\n" + "=" * 80)
print("第二阶段总结")
print("=" * 80)
print("""
核心要点：
1. ✅ 数值约束: gt, ge, lt, le
2. ✅ 字符串约束: min_length, max_length, pattern
3. ✅ Field(...) 表示必需字段
4. ✅ Field(default=...) 表示可选字段
5. ✅ 特殊类型: EmailStr, HttpUrl（需要额外安装）

常用参数：
- description: 字段描述
- examples: 示例值
- alias: 别名（下一章节详细讲）
- default: 默认值
- default_factory: 动态默认值（下一章节详细讲）

易错点：
❌ Field("value") - 错误！必须用 Field(default="value")
❌ gt=0 和 ge=0 混淆 - gt 不包含0，ge 包含0
✅ 记住：Field 参数都要用关键字参数

下一步：学习自定义验证器（03_validators.py）
""")

