"""
Pydantic V2 学习 - 第四阶段：嵌套模型和复杂类型
学习时间：1.5小时
重点：处理嵌套关系、列表、字典等复杂数据结构
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Set, Tuple, Optional, Union
from datetime import datetime

print("=" * 80)
print("第四阶段：嵌套模型和复杂类型")
print("=" * 80)
print()

# ===== 1. 基础嵌套模型 =====
print("1. 基础嵌套模型")
print("-" * 80)

class Address(BaseModel):
    """地址模型"""
    street: str
    city: str
    province: str
    country: str = "中国"
    postal_code: Optional[str] = None

class Person(BaseModel):
    """人员模型 - 包含地址"""
    name: str
    age: int
    address: Address  # 嵌套的地址模型

# 创建嵌套实例
person_data = {
    "name": "张三",
    "age": 30,
    "address": {
        "street": "中关村大街1号",
        "city": "北京",
        "province": "北京",
        "postal_code": "100000"
    }
}

person = Person.model_validate(person_data)
print(f"✅ 创建成功:")
print(f"   姓名: {person.name}")
print(f"   地址: {person.address.city}, {person.address.street}")
print()

# 转换为字典
print("转换为字典:")
print(person.model_dump())
print()

# 转换为 JSON
print("转换为 JSON (格式化):")
print(person.model_dump_json(indent=2))
print()


# ===== 2. 列表类型 =====
print("\n2. 列表类型 - List[T]")
print("-" * 80)

class Company(BaseModel):
    """公司模型"""
    name: str
    founded_year: int

class Employee(BaseModel):
    """员工模型 - 包含公司列表"""
    name: str
    email: str
    companies: List[Company]  # 公司列表
    skills: List[str]  # 字符串列表

# 测试数据
employee_data = {
    "name": "李四",
    "email": "lisi@example.com",
    "companies": [
        {"name": "腾讯", "founded_year": 1998},
        {"name": "阿里巴巴", "founded_year": 1999}
    ],
    "skills": ["Python", "JavaScript", "Go"]
}

employee = Employee.model_validate(employee_data)
print(f"✅ 员工信息:")
print(f"   姓名: {employee.name}")
print(f"   工作经历: {len(employee.companies)} 家公司")
for company in employee.companies:
    print(f"     - {company.name} (成立于 {company.founded_year})")
print(f"   技能: {', '.join(employee.skills)}")
print()


# ===== 3. 字典类型 =====
print("\n3. 字典类型 - Dict[K, V]")
print("-" * 80)

class Product(BaseModel):
    """产品模型"""
    name: str
    price: float
    metadata: Dict[str, str]  # 字符串键值对
    specifications: Dict[str, Union[str, int, float]]  # 混合类型值
    tags: Dict[str, bool]  # 标签（键-布尔值对）

product_data = {
    "name": "iPhone 15 Pro",
    "price": 7999.00,
    "metadata": {
        "brand": "Apple",
        "origin": "美国",
        "warranty": "1年"
    },
    "specifications": {
        "screen_size": "6.1英寸",
        "storage": 256,
        "weight": 187.0
    },
    "tags": {
        "5g": True,
        "waterproof": True,
        "discontinued": False
    }
}

product = Product.model_validate(product_data)
print(f"✅ 产品信息:")
print(f"   名称: {product.name}")
print(f"   规格:")
for key, value in product.specifications.items():
    print(f"     - {key}: {value}")
print()


# ===== 4. 集合和元组 =====
print("\n4. 集合和元组 - Set, Tuple")
print("-" * 80)

class Article(BaseModel):
    """文章模型"""
    title: str
    tags: Set[str]  # 自动去重的标签集合
    coordinates: Tuple[float, float]  # 固定长度的元组（经纬度）
    categories: Set[str] = Field(default_factory=set)  # 空集合默认值

article_data = {
    "title": "Pydantic 教程",
    "tags": ["Python", "Pydantic", "Python", "教程"],  # Python 重复了
    "coordinates": [39.9042, 116.4074],  # 北京坐标
    "categories": {"技术", "编程", "Python"}
}

article = Article.model_validate(article_data)
print(f"✅ 文章信息:")
print(f"   标题: {article.title}")
print(f"   标签: {article.tags}")  # Python 只出现一次
print(f"   坐标: {article.coordinates}")
print(f"   分类: {article.categories}")
print()


# ===== 5. Optional 和 Union 类型 =====
print("\n5. Optional 和 Union 类型")
print("-" * 80)

class User(BaseModel):
    """用户模型 - 演示可选和联合类型"""
    id: int
    name: str
    nickname: Optional[str] = None  # 可选字段
    age: Optional[int] = None
    contact: Union[str, int]  # 可以是字符串或整数
    status: Union[str, int, None] = None  # 可以是字符串、整数或 None

# 测试不同的数据
test_users = [
    {"id": 1, "name": "张三", "contact": "zhangsan@example.com"},
    {"id": 2, "name": "李四", "nickname": "小李", "age": 25, "contact": 13800138000},
    {"id": 3, "name": "王五", "contact": "wangwu@example.com", "status": "active"}
]

for user_data in test_users:
    user = User.model_validate(user_data)
    print(f"✅ 用户 {user.id}: {user.name}")
    print(f"   nickname: {user.nickname}")
    print(f"   contact: {user.contact} (类型: {type(user.contact).__name__})")
print()


# ===== 6. 深度嵌套示例 =====
print("\n6. 深度嵌套示例")
print("-" * 80)

class Tag(BaseModel):
    """标签"""
    name: str
    color: str = "blue"

class Comment(BaseModel):
    """评论"""
    author: str
    content: str
    created_at: datetime
    likes: int = 0

class Post(BaseModel):
    """帖子"""
    title: str
    content: str
    author: str
    tags: List[Tag]
    comments: List[Comment]
    metadata: Dict[str, str]

class Blog(BaseModel):
    """博客 - 包含多个帖子"""
    name: str
    owner: Person  # 引用之前定义的 Person
    posts: List[Post]

# 构建复杂数据
blog_data = {
    "name": "我的技术博客",
    "owner": {
        "name": "博主张三",
        "age": 28,
        "address": {
            "street": "科技路100号",
            "city": "深圳",
            "province": "广东"
        }
    },
    "posts": [
        {
            "title": "Pydantic V2 入门",
            "content": "这是一篇关于 Pydantic V2 的教程...",
            "author": "张三",
            "tags": [
                {"name": "Python", "color": "blue"},
                {"name": "Pydantic", "color": "green"}
            ],
            "comments": [
                {
                    "author": "读者A",
                    "content": "写得很好！",
                    "created_at": "2024-01-01T10:00:00",
                    "likes": 10
                }
            ],
            "metadata": {
                "category": "教程",
                "difficulty": "入门"
            }
        }
    ]
}

blog = Blog.model_validate(blog_data)
print(f"✅ 博客信息:")
print(f"   名称: {blog.name}")
print(f"   博主: {blog.owner.name} (来自 {blog.owner.address.city})")
print(f"   文章数: {len(blog.posts)}")
for post in blog.posts:
    print(f"     - {post.title}")
    print(f"       标签: {', '.join(tag.name for tag in post.tags)}")
    print(f"       评论数: {len(post.comments)}")
print()


# ===== 7. 易错点：可变默认值 =====
print("\n7. ⚠️  易错点：可变默认值")
print("-" * 80)

print("❌ 错误示例（会导致问题）:")
print("""
class WrongModel(BaseModel):
    tags: List[str] = []  # 危险！所有实例共享同一个列表
    scores: Dict[str, int] = {}  # 危险！
""")
print()

print("✅ 正确写法：使用 default_factory")
print("""
from pydantic import Field

class CorrectModel(BaseModel):
    tags: List[str] = Field(default_factory=list)
    scores: Dict[str, int] = Field(default_factory=dict)
    metadata: Dict[str, str] = Field(default_factory=lambda: {"version": "1.0"})
""")
print()

class CorrectModel(BaseModel):
    """正确的可变默认值"""
    tags: List[str] = Field(default_factory=list)
    scores: Dict[str, int] = Field(default_factory=dict)
    metadata: Dict[str, str] = Field(default_factory=lambda: {"version": "1.0"})

# 创建多个实例
obj1 = CorrectModel()
obj2 = CorrectModel()

obj1.tags.append("tag1")
obj2.tags.append("tag2")

print(f"obj1.tags: {obj1.tags}")  # ['tag1']
print(f"obj2.tags: {obj2.tags}")  # ['tag2']
print(f"obj1.metadata: {obj1.metadata}")  # {'version': '1.0'}
print("✅ 每个实例都有独立的列表和字典")
print()


# ===== 8. 实战练习：构建电商订单系统 =====
print("\n8. 实战练习：电商订单系统")
print("-" * 80)

class ProductItem(BaseModel):
    """商品项"""
    product_id: int
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    
    @property
    def subtotal(self) -> float:
        """计算小计"""
        return self.price * self.quantity

class ShippingAddress(BaseModel):
    """配送地址"""
    recipient: str
    phone: str
    address: str
    city: str
    province: str
    postal_code: str

class Order(BaseModel):
    """订单"""
    order_id: str
    customer_name: str
    items: List[ProductItem] = Field(min_length=1)  # 至少一个商品
    shipping_address: ShippingAddress
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    @property
    def total_amount(self) -> float:
        """计算订单总金额"""
        return sum(item.subtotal for item in self.items)
    
    @property
    def item_count(self) -> int:
        """商品总数"""
        return sum(item.quantity for item in self.items)

# 创建订单
order_data = {
    "order_id": "ORD20240101001",
    "customer_name": "王女士",
    "items": [
        {
            "product_id": 1001,
            "name": "iPhone 15",
            "price": 5999.00,
            "quantity": 1
        },
        {
            "product_id": 1002,
            "name": "AirPods Pro",
            "price": 1999.00,
            "quantity": 2
        }
    ],
    "shipping_address": {
        "recipient": "王女士",
        "phone": "13800138000",
        "address": "中关村大街1号",
        "city": "北京",
        "province": "北京",
        "postal_code": "100000"
    },
    "notes": "请在工作日配送"
}

order = Order.model_validate(order_data)
print(f"✅ 订单创建成功:")
print(f"   订单号: {order.order_id}")
print(f"   客户: {order.customer_name}")
print(f"   商品:")
for item in order.items:
    print(f"     - {item.name} x{item.quantity} = ¥{item.subtotal:.2f}")
print(f"   商品总数: {order.item_count} 件")
print(f"   订单总金额: ¥{order.total_amount:.2f}")
print(f"   配送地址: {order.shipping_address.city}, {order.shipping_address.address}")
print(f"   备注: {order.notes}")
print()

# 输出为 JSON
print("订单 JSON (部分):")
print(order.model_dump_json(indent=2, include={'order_id', 'customer_name', 'status'}))
print()


# ===== 总结 =====
print("\n" + "=" * 80)
print("第四阶段总结")
print("=" * 80)
print("""
核心要点：
1. ✅ 嵌套模型：在一个模型中引用另一个模型
2. ✅ List[T]：列表类型
3. ✅ Dict[K, V]：字典类型
4. ✅ Set[T]：集合类型（自动去重）
5. ✅ Tuple[T1, T2, ...]：固定长度元组
6. ✅ Optional[T]：可选类型（等同于 T | None）
7. ✅ Union[T1, T2]：联合类型（可以是多种类型之一）

类型速查表：
┌──────────────────┬─────────────────────┬──────────────────┐
│ Python 类型      │ 用途                │ 示例             │
├──────────────────┼─────────────────────┼──────────────────┤
│ List[str]        │ 字符串列表          │ ["a", "b", "c"]  │
│ Dict[str, int]   │ 字符串到整数的映射  │ {"age": 25}      │
│ Set[int]         │ 整数集合（去重）    │ {1, 2, 3}        │
│ Tuple[int, str]  │ 固定类型元组        │ (1, "hello")     │
│ Optional[str]    │ 可选字符串          │ "hello" 或 None  │
│ Union[str, int]  │ 字符串或整数        │ "text" 或 123    │
└──────────────────┴─────────────────────┴──────────────────┘

易错点：
❌ 可变默认值：tags: List[str] = []
✅ 使用 default_factory：tags: List[str] = Field(default_factory=list)

❌ 忘记导入类型：from typing import List, Dict, Optional
✅ 总是从 typing 导入需要的类型

技巧：
• 深度嵌套时，先定义内层模型，再定义外层模型
• 使用 @property 添加计算属性
• model_dump() 会递归转换所有嵌套模型

下一步：学习 Model Config 配置（05_model_config.py）
""")

