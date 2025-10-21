"""
Pydantic V2 学习 - 第三阶段：自定义验证器
学习时间：1小时
重点：掌握 field_validator 和 model_validator，实现复杂验证逻辑
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
import re

print("=" * 80)
print("第三阶段：自定义验证器")
print("=" * 80)
print()

# ===== 1. field_validator 基础 =====
print("1. field_validator 基础 - 单字段验证")
print("-" * 80)

class User(BaseModel):
    """用户模型 - 演示字段验证器"""
    username: str
    email: str
    age: int
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        """验证用户名只包含字母和数字"""
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v.lower()  # 转换为小写
    
    @field_validator('age')
    @classmethod
    def age_must_be_adult(cls, v: int) -> int:
        """验证年龄必须成年"""
        if v < 18:
            raise ValueError('年龄必须大于等于18岁')
        return v

# 测试
try:
    user1 = User(username="ZhangSan123", email="test@example.com", age=25)
    print(f"✅ 创建成功: {user1}")
    print(f"   注意：username 被转换为小写: {user1.username}")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

# 测试失败情况
try:
    user2 = User(username="zhang-san", email="test@example.com", age=25)
    print(f"✅ 创建成功: {user2}")
except Exception as e:
    print(f"❌ 用户名包含特殊字符: {e}")
print()

try:
    user3 = User(username="zhangsan", email="test@example.com", age=17)
    print(f"✅ 创建成功: {user3}")
except Exception as e:
    print(f"❌ 年龄不足18岁: {e}")
print()


# ===== 2. 验证多个字段 =====
print("\n2. 验证多个字段")
print("-" * 80)

class Product(BaseModel):
    """产品模型 - 同一个验证器验证多个字段"""
    name: str
    description: str
    price: float
    
    @field_validator('name', 'description')
    @classmethod
    def not_empty(cls, v: str) -> str:
        """验证字符串不能为空或只有空格"""
        if not v or not v.strip():
            raise ValueError('字段不能为空')
        return v.strip()

# 测试
try:
    product = Product(name="  iPhone  ", description="  好产品  ", price=5999)
    print(f"✅ 创建成功: {product}")
    print(f"   注意：name 和 description 的空格被去除")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()


# ===== 3. model_validator - 跨字段验证 =====
print("\n3. model_validator - 跨字段验证")
print("-" * 80)

class PasswordChange(BaseModel):
    """密码修改 - 演示跨字段验证"""
    password: str = Field(min_length=8)
    password_confirm: str
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'PasswordChange':
        """验证两次密码是否一致"""
        if self.password != self.password_confirm:
            raise ValueError('两次输入的密码不一致')
        return self

# 测试成功
try:
    pwd1 = PasswordChange(password="12345678", password_confirm="12345678")
    print(f"✅ 密码一致: 验证通过")
except Exception as e:
    print(f"❌ 验证失败: {e}")
print()

# 测试失败
try:
    pwd2 = PasswordChange(password="12345678", password_confirm="87654321")
    print(f"✅ 创建成功")
except Exception as e:
    print(f"❌ 密码不一致: {e}")
print()


# ===== 4. mode='before' vs mode='after' =====
print("\n4. mode='before' vs mode='after' 的区别")
print("-" * 80)

class Example1(BaseModel):
    """mode='before' - 在 Pydantic 解析前验证"""
    value: int
    
    @model_validator(mode='before')
    @classmethod
    def validate_before(cls, data):
        """
        mode='before': 
        - 接收原始输入数据（字典）
        - 在类型转换之前执行
        - 可以修改原始数据
        """
        print(f"   [before] 接收到的数据类型: {type(data)}")
        print(f"   [before] 数据内容: {data}")
        
        # 可以在这里预处理数据
        if isinstance(data, dict) and 'value' in data:
            # 例如：将字符串转换为整数
            if isinstance(data['value'], str):
                data['value'] = int(data['value'])
        
        return data

class Example2(BaseModel):
    """mode='after' - 在 Pydantic 解析后验证"""
    value: int
    
    @model_validator(mode='after')
    def validate_after(self) -> 'Example2':
        """
        mode='after':
        - 接收模型实例（self）
        - 在类型转换之后执行
        - 可以访问所有字段
        """
        print(f"   [after] 接收到的数据类型: {type(self)}")
        print(f"   [after] value 的值: {self.value}")
        return self

print("测试 mode='before':")
ex1 = Example1.model_validate({"value": "123"})  # 字符串会被转换
print()

print("测试 mode='after':")
ex2 = Example2.model_validate({"value": 123})
print()


# ===== 5. 复杂验证示例 =====
print("\n5. 复杂验证示例：用户注册")
print("-" * 80)

class UserRegistration(BaseModel):
    """完整的用户注册验证"""
    username: str = Field(min_length=3, max_length=20)
    email: str
    password: str = Field(min_length=8)
    password_confirm: str
    age: int
    phone: Optional[str] = None
    
    # 字段验证器 1: 用户名规则
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """用户名只能包含字母、数字、下划线"""
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v.lower()
    
    # 字段验证器 2: 邮箱规则
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """简单的邮箱验证"""
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('邮箱格式不正确')
        return v.lower()
    
    # 字段验证器 3: 密码强度
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """密码必须包含字母和数字"""
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_letter and has_digit):
            raise ValueError('密码必须同时包含字母和数字')
        return v
    
    # 字段验证器 4: 年龄检查
    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        """年龄必须在 18-120 之间"""
        if not (18 <= v <= 120):
            raise ValueError('年龄必须在18-120岁之间')
        return v
    
    # 字段验证器 5: 手机号验证
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """手机号格式验证（可选）"""
        if v is None:
            return v
        if not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式不正确')
        return v
    
    # 模型验证器: 密码一致性
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegistration':
        """检查两次密码是否一致"""
        if self.password != self.password_confirm:
            raise ValueError('两次输入的密码不一致')
        return self

# 测试数据
test_cases = [
    {
        "name": "正常注册",
        "data": {
            "username": "ZhangSan_123",
            "email": "ZhangSan@Example.COM",
            "password": "Pass1234",
            "password_confirm": "Pass1234",
            "age": 25,
            "phone": "13800138000"
        }
    },
    {
        "name": "用户名包含特殊字符",
        "data": {
            "username": "zhang-san",
            "email": "test@example.com",
            "password": "Pass1234",
            "password_confirm": "Pass1234",
            "age": 25
        }
    },
    {
        "name": "密码太弱（纯数字）",
        "data": {
            "username": "zhangsan",
            "email": "test@example.com",
            "password": "12345678",
            "password_confirm": "12345678",
            "age": 25
        }
    },
    {
        "name": "密码不一致",
        "data": {
            "username": "zhangsan",
            "email": "test@example.com",
            "password": "Pass1234",
            "password_confirm": "Pass5678",
            "age": 25
        }
    }
]

for test in test_cases:
    try:
        user = UserRegistration.model_validate(test["data"])
        print(f"✅ {test['name']}")
        print(f"   username: {user.username} (转为小写)")
        print(f"   email: {user.email} (转为小写)")
    except Exception as e:
        print(f"❌ {test['name']}: {e}")
print()


# ===== 6. 易错点演示 =====
print("\n6. ⚠️  常见易错点")
print("-" * 80)

print("易错点 1: V2 使用 @field_validator，不是 @validator")
print("-" * 40)
print("❌ 错误 (V1):")
print("   @validator('field_name')")
print()
print("✅ 正确 (V2):")
print("   @field_validator('field_name')")
print("   @classmethod")
print()

print("易错点 2: field_validator 必须添加 @classmethod")
print("-" * 40)
print("❌ 错误:")
print("   @field_validator('name')")
print("   def validate_name(cls, v):  # 缺少 @classmethod")
print("       return v")
print()
print("✅ 正确:")
print("   @field_validator('name')")
print("   @classmethod")
print("   def validate_name(cls, v: str) -> str:")
print("       return v")
print()

print("易错点 3: 验证器必须返回值")
print("-" * 40)
print("❌ 错误:")
print("   @field_validator('name')")
print("   @classmethod")
print("   def validate_name(cls, v):")
print("       if not v:")
print("           raise ValueError('错误')")
print("       # 忘记 return v")
print()
print("✅ 正确:")
print("   @field_validator('name')")
print("   @classmethod")
print("   def validate_name(cls, v: str) -> str:")
print("       if not v:")
print("           raise ValueError('错误')")
print("       return v  # 必须返回！")
print()

print("易错点 4: model_validator 的 mode 参数")
print("-" * 40)
print("mode='before': 接收原始数据（dict），在类型转换前")
print("mode='after':  接收模型实例（self），在类型转换后")
print("选择哪个？")
print("  - 需要预处理原始数据 → 用 before")
print("  - 需要访问多个字段进行验证 → 用 after")
print()


# ===== 总结 =====
print("\n" + "=" * 80)
print("第三阶段总结")
print("=" * 80)
print("""
核心要点：
1. ✅ @field_validator('field') - 单字段验证（V2新语法）
2. ✅ 必须添加 @classmethod 装饰器
3. ✅ 验证器必须返回值
4. ✅ @model_validator(mode='after') - 跨字段验证

两种验证器对比：
┌─────────────────┬────────────────┬──────────────────┐
│ 特性            │ field_validator│ model_validator  │
├─────────────────┼────────────────┼──────────────────┤
│ 验证范围        │ 单个/多个字段  │ 整个模型         │
│ 接收参数        │ 字段值         │ 原始数据或模型   │
│ 使用场景        │ 单字段规则     │ 跨字段逻辑       │
│ 需要@classmethod│ 是             │ mode=before时是  │
└─────────────────┴────────────────┴──────────────────┘

mode 选择：
- mode='before': 原始数据预处理
- mode='after':  模型实例验证（最常用）

易错点：
❌ 使用 @validator（V1语法）
❌ 忘记 @classmethod
❌ 忘记 return 值
❌ 混淆 before 和 after 的用法
✅ V2 统一使用 @field_validator 和 @model_validator

下一步：学习嵌套模型和复杂类型（04_nested_models.py）
""")

