"""
Pydantic V2 学习 - 第七阶段：实战练习
学习时间：1小时
重点：综合应用所学知识，构建真实场景的数据模型
"""

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, field_serializer
from typing import List, Dict, Optional, Union
from datetime import datetime, date
from enum import Enum

print("=" * 80)
print("第七阶段：实战练习")
print("=" * 80)
print()

# ===== 实战 1: 用户认证系统 =====
print("实战 1: 用户认证系统")
print("=" * 80)

class UserRole(str, Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class UserRegister(BaseModel):
    """用户注册模型"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_min_length=1
    )
    
    username: str = Field(min_length=3, max_length=20, description="用户名")
    email: str = Field(description="邮箱")
    password: str = Field(min_length=8, max_length=50, description="密码")
    password_confirm: str = Field(description="确认密码")
    phone: Optional[str] = Field(None, pattern=r'^1[3-9]\d{9}$', description="手机号")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """用户名只能包含字母、数字、下划线"""
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v.lower()
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """邮箱验证"""
        import re
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('邮箱格式不正确')
        return v.lower()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """密码强度验证"""
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError('密码必须包含大小写字母和数字')
        return v
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegister':
        """检查密码一致性"""
        if self.password != self.password_confirm:
            raise ValueError('两次输入的密码不一致')
        return self

class UserLogin(BaseModel):
    """用户登录模型"""
    username_or_email: str = Field(description="用户名或邮箱")
    password: str = Field(description="密码")
    remember_me: bool = Field(default=False, description="记住我")

class UserResponse(BaseModel):
    """用户响应模型（不包含敏感信息）"""
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
    
    user_id: int = Field(alias="id", serialization_alias="userId")
    username: str
    email: str
    phone: Optional[str] = None
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now, serialization_alias="createdAt")
    
    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

# 测试注册
print("测试用户注册:")
register_data = {
    "username": "  ZhangSan123  ",
    "email": "  ZhangSan@Example.COM  ",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "phone": "13800138000"
}

try:
    user_register = UserRegister.model_validate(register_data)
    print(f"✅ 注册成功:")
    print(f"   用户名: {user_register.username} (已转为小写)")
    print(f"   邮箱: {user_register.email} (已转为小写)")
except Exception as e:
    print(f"❌ 注册失败: {e}")
print()

# 测试响应
print("用户响应示例:")
user_response = UserResponse(
    id=1,
    username="zhangsan123",
    email="zhangsan@example.com",
    phone="13800138000",
    role=UserRole.ADMIN
)
print(user_response.model_dump_json(by_alias=True, indent=2))
print()


# ===== 实战 2: 电商商品管理 =====
print("\n实战 2: 电商商品管理")
print("=" * 80)

class ProductCategory(str, Enum):
    """商品分类"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"

class ProductSpec(BaseModel):
    """商品规格"""
    name: str = Field(description="规格名称")
    value: Union[str, int, float] = Field(description="规格值")

class ProductImage(BaseModel):
    """商品图片"""
    url: str = Field(description="图片URL")
    alt: str = Field(default="", description="图片描述")
    is_primary: bool = Field(default=False, description="是否主图")

class ProductCreate(BaseModel):
    """创建商品模型"""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )
    
    name: str = Field(min_length=1, max_length=200, description="商品名称")
    description: str = Field(max_length=2000, description="商品描述")
    category: ProductCategory = Field(description="商品分类")
    price: float = Field(gt=0, description="价格（元）")
    stock: int = Field(ge=0, description="库存")
    images: List[ProductImage] = Field(min_length=1, description="商品图片")
    specifications: List[ProductSpec] = Field(default_factory=list, description="商品规格")
    tags: List[str] = Field(default_factory=list, description="标签")
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        """价格最多两位小数"""
        return round(v, 2)
    
    @model_validator(mode='after')
    def check_images(self) -> 'ProductCreate':
        """确保至少有一张主图"""
        has_primary = any(img.is_primary for img in self.images)
        if not has_primary:
            # 自动设置第一张为主图
            self.images[0].is_primary = True
        return self

class ProductResponse(BaseModel):
    """商品响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(serialization_alias="productId")
    name: str
    description: str
    category: ProductCategory
    price: float
    stock: int
    images: List[ProductImage]
    specifications: List[ProductSpec]
    tags: List[str]
    is_available: bool = Field(default=True, serialization_alias="isAvailable")
    created_at: datetime = Field(default_factory=datetime.now, serialization_alias="createdAt")
    
    @field_serializer('price')
    def serialize_price(self, value: float) -> str:
        return f"{value:.2f}"
    
    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

# 测试创建商品
print("创建商品:")
product_data = {
    "name": "iPhone 15 Pro",
    "description": "最新款 iPhone，搭载 A17 Pro 芯片",
    "category": "electronics",
    "price": 7999.999,  # 会被四舍五入
    "stock": 100,
    "images": [
        {"url": "https://example.com/img1.jpg", "alt": "正面图"},
        {"url": "https://example.com/img2.jpg", "alt": "背面图", "is_primary": False}
    ],
    "specifications": [
        {"name": "屏幕尺寸", "value": "6.1英寸"},
        {"name": "存储", "value": 256},
        {"name": "重量", "value": 187.0}
    ],
    "tags": ["5G", "防水", "快充"]
}

try:
    product = ProductCreate.model_validate(product_data)
    print(f"✅ 商品创建成功:")
    print(f"   名称: {product.name}")
    print(f"   价格: ¥{product.price} (已四舍五入到两位小数)")
    print(f"   主图: {[img.url for img in product.images if img.is_primary]}")
except Exception as e:
    print(f"❌ 创建失败: {e}")
print()

# 商品响应
print("商品响应 JSON:")
product_response = ProductResponse(
    id=1001,
    name=product.name,
    description=product.description,
    category=product.category,
    price=product.price,
    stock=product.stock,
    images=product.images,
    specifications=product.specifications,
    tags=product.tags
)
print(product_response.model_dump_json(by_alias=True, indent=2))
print()


# ===== 实战 3: API 分页响应 =====
print("\n实战 3: API 分页响应")
print("=" * 80)

from typing import Generic, TypeVar

T = TypeVar('T')

class PageRequest(BaseModel):
    """分页请求"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")
    sort_by: Optional[str] = Field(None, description="排序字段")
    order: str = Field(default="asc", pattern="^(asc|desc)$", description="排序方向")

class PageResponse(BaseModel, Generic[T]):
    """分页响应（泛型）"""
    items: List[T] = Field(description="数据列表")
    total: int = Field(description="总数")
    page: int = Field(description="当前页")
    page_size: int = Field(serialization_alias="pageSize", description="每页数量")
    total_pages: int = Field(serialization_alias="totalPages", description="总页数")
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int) -> 'PageResponse[T]':
        """工厂方法"""
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

# 使用示例
print("分页请求示例:")
page_request = PageRequest(page=2, page_size=20, sort_by="created_at", order="desc")
print(f"  {page_request.model_dump()}")
print()

print("分页响应示例:")
# 模拟用户列表
users = [
    UserResponse(id=i, username=f"user{i}", email=f"user{i}@example.com")
    for i in range(1, 6)
]
page_response = PageResponse[UserResponse].create(
    items=users,
    total=50,
    page=2,
    page_size=5
)
print(f"  总数: {page_response.total}")
print(f"  当前页: {page_response.page}/{page_response.total_pages}")
print(f"  数据: {len(page_response.items)} 条")
print()


# ===== 实战 4: 配置管理 =====
print("\n实战 4: 应用配置管理")
print("=" * 80)

class DatabaseConfig(BaseModel):
    """数据库配置"""
    host: str = Field(default="localhost")
    port: int = Field(default=3306, ge=1, le=65535)
    username: str
    password: str = Field(exclude=True)  # 不序列化密码
    database: str
    
    @property
    def connection_string(self) -> str:
        """生成连接字符串（隐藏密码）"""
        return f"mysql://{self.username}:****@{self.host}:{self.port}/{self.database}"

class RedisConfig(BaseModel):
    """Redis 配置"""
    host: str = Field(default="localhost")
    port: int = Field(default=6379, ge=1, le=65535)
    db: int = Field(default=0, ge=0)
    password: Optional[str] = Field(None, exclude=True)

class AppConfig(BaseModel):
    """应用配置"""
    model_config = ConfigDict(
        frozen=True,  # 配置不可修改
        validate_assignment=True,
        extra='forbid'  # 不允许额外字段
    )
    
    app_name: str = Field(default="MyApp")
    debug: bool = Field(default=False)
    secret_key: str = Field(exclude=True)  # 不序列化
    database: DatabaseConfig
    redis: RedisConfig
    allowed_hosts: List[str] = Field(default_factory=list)
    
    @model_validator(mode='after')
    def check_production_settings(self) -> 'AppConfig':
        """生产环境检查"""
        if not self.debug and not self.allowed_hosts:
            raise ValueError('生产环境必须设置 allowed_hosts')
        return self

# 配置示例
print("加载应用配置:")
config_data = {
    "app_name": "我的应用",
    "debug": False,
    "secret_key": "super-secret-key-here",
    "database": {
        "host": "db.example.com",
        "port": 3306,
        "username": "root",
        "password": "db_password",
        "database": "myapp"
    },
    "redis": {
        "host": "redis.example.com",
        "db": 1
    },
    "allowed_hosts": ["example.com", "www.example.com"]
}

try:
    config = AppConfig.model_validate(config_data)
    print(f"✅ 配置加载成功:")
    print(f"   应用: {config.app_name}")
    print(f"   数据库: {config.database.connection_string}")
    print(f"   允许的主机: {config.allowed_hosts}")
    print()
    
    # 配置是不可变的
    print("尝试修改配置:")
    try:
        config.debug = True
    except Exception:
        print("  ❌ 失败（正确的！配置是不可变的）")
    print()
    
    # 导出配置（不包含敏感信息）
    print("导出配置（排除敏感信息）:")
    exported_config = config.model_dump()
    print(f"  {exported_config}")
    
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
print()


# ===== 总结 =====
print("\n" + "=" * 80)
print("第七阶段总结")
print("=" * 80)
print("""
实战要点回顾：

1. 用户认证系统：
   ✓ 字段验证（用户名、邮箱、密码）
   ✓ 跨字段验证（密码确认）
   ✓ 敏感信息处理
   ✓ 响应格式化

2. 电商商品管理：
   ✓ 枚举类型使用
   ✓ 嵌套模型
   ✓ 列表验证
   ✓ 自动数据修正

3. API 分页响应：
   ✓ 泛型模型
   ✓ 工厂方法
   ✓ 别名使用

4. 配置管理：
   ✓ 不可变模型
   ✓ 排除敏感字段
   ✓ 生产环境检查
   ✓ 嵌套配置

最佳实践：
• 输入模型：严格验证（validate_assignment, str_strip_whitespace）
• 输出模型：格式化数据（field_serializer, by_alias）
• 配置模型：不可变（frozen=True）
• API 模型：清晰的别名（alias, serialization_alias）

下一步：查看常见错误对比（08_common_mistakes.py）
""")

