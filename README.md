# Pydantic V2 学习项目 🚀

这是一个完整的 Pydantic V2 学习项目，包含系统的教程、示例代码和实战练习。

## 📚 项目结构

```
pydantic-v2/
├── main.py                          # 快速示例
├── learning/                        # 学习教程目录
│   ├── README_LEARNING.md          # 📖 完整学习指南
│   ├── QUICK_REFERENCE.md          # ⚡ 速查表
│   ├── 01_basics.py                # 第1章：V2基础
│   ├── 02_field_constraints.py     # 第2章：Field约束
│   ├── 03_validators.py            # 第3章：自定义验证器
│   ├── 04_nested_models.py         # 第4章：嵌套模型
│   ├── 05_model_config.py          # 第5章：配置
│   ├── 06_aliases_serialization.py # 第6章：别名和序列化
│   ├── 07_practical.py             # 第7章：实战练习
│   └── 08_common_mistakes.py       # 第8章：常见错误
└── README.md                        # 本文件
```

## 🎯 快速开始

### 1. 安装依赖

```bash
# 使用 pip
pip install pydantic

# 或使用 uv
uv pip install pydantic
```

### 2. 运行示例

```bash
# 快速体验
python main.py

# 系统学习（按顺序）
python learning/01_basics.py
python learning/02_field_constraints.py
python learning/03_validators.py
# ... 依此类推
```

### 3. 查看学习指南

- **完整教程**：[learning/README_LEARNING.md](learning/README_LEARNING.md)
- **速查表**：[learning/QUICK_REFERENCE.md](learning/QUICK_REFERENCE.md)

## 📖 学习路径

| 章节 | 文件 | 主题 | 时间 |
|------|------|------|------|
| 1 | `01_basics.py` | V2 基础 | 1h |
| 2 | `02_field_constraints.py` | Field 约束 | 1.5h |
| 3 | `03_validators.py` | 自定义验证器 | 1h |
| 4 | `04_nested_models.py` | 嵌套模型 | 1.5h |
| 5 | `05_model_config.py` | Model Config | 1h |
| 6 | `06_aliases_serialization.py` | 别名和序列化 | 1h |
| 7 | `07_practical.py` | 实战练习 | 1h |
| 8 | `08_common_mistakes.py` | 常见错误 | 0.5h |

**总计：约 8.5 小时**

## 🌟 核心特性

### V2 核心方法

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# 创建实例
user = User(name="张三", age=25)
user = User.model_validate({"name": "张三", "age": 25})
user = User.model_validate_json('{"name": "张三", "age": 25}')

# 序列化
user.model_dump()          # Python dict
user.model_dump_json()     # JSON string
```

### Field 约束

```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)  # 大于 0
    stock: int = Field(ge=0)    # 大于等于 0
```

### 自定义验证

```python
from pydantic import field_validator, model_validator

class UserRegister(BaseModel):
    username: str
    password: str
    password_confirm: str
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        return v.lower()
    
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegister':
        if self.password != self.password_confirm:
            raise ValueError('密码不一致')
        return self
```

## 💡 V1 → V2 迁移

| V1 | V2 |
|----|----| 
| `dict()` | `model_dump()` |
| `json()` | `model_dump_json()` |
| `parse_obj()` | `model_validate()` |
| `parse_raw()` | `model_validate_json()` |
| `copy()` | `model_copy()` |
| `@validator` | `@field_validator` |
| `class Config:` | `model_config = ConfigDict()` |
| `orm_mode` | `from_attributes` |

## 📚 学习内容

### 第1章：V2 基础
- ✅ 核心方法：validate、dump、copy
- ✅ V1/V2 对比
- ✅ 基础模型定义

### 第2章：Field 约束
- ✅ 数值约束：gt、ge、lt、le
- ✅ 字符串约束：min_length、max_length、pattern
- ✅ 特殊类型：EmailStr、HttpUrl

### 第3章：自定义验证器
- ✅ @field_validator - 单字段验证
- ✅ @model_validator - 跨字段验证
- ✅ mode='before' vs mode='after'

### 第4章：嵌套模型
- ✅ List、Dict、Set、Tuple
- ✅ Optional、Union
- ✅ 深度嵌套处理

### 第5章：Model Config
- ✅ ConfigDict 配置
- ✅ 字符串处理
- ✅ 验证行为
- ✅ ORM 支持

### 第6章：别名和序列化
- ✅ alias 和 serialization_alias
- ✅ include/exclude
- ✅ 自定义序列化器

### 第7章：实战练习
- ✅ 用户认证系统
- ✅ 电商商品管理
- ✅ API 分页响应
- ✅ 配置管理

### 第8章：常见错误
- ✅ V1/V2 方法混淆
- ✅ Field 参数错误
- ✅ 验证器常见问题
- ✅ 类型使用错误

## 🎓 学习建议

1. **按顺序学习** - 知识点是递进的
2. **动手实践** - 修改代码，尝试不同参数
3. **查看输出** - 每个示例都有详细输出
4. **做笔记** - 记录易错点
5. **完成练习** - 第7章有完整实战

## 📝 快速参考

### 创建模型

```python
user = User(name="张三", age=25)
user = User.model_validate(data_dict)
user = User.model_validate_json(json_string)
```

### 序列化

```python
user.model_dump()                          # dict
user.model_dump(exclude={'password'})      # 排除字段
user.model_dump(exclude_none=True)         # 排除 None
user.model_dump_json(indent=2)             # JSON
```

### 验证器

```python
@field_validator('field_name')
@classmethod
def validate_field(cls, v: Type) -> Type:
    # 验证逻辑
    return v  # 必须返回值！

@model_validator(mode='after')
def validate_model(self) -> 'ModelName':
    # 跨字段验证
    return self
```

### 配置

```python
model_config = ConfigDict(
    str_strip_whitespace=True,
    validate_assignment=True,
    from_attributes=True
)
```

## 🔗 相关资源

- [Pydantic 官方文档](https://docs.pydantic.dev/latest/)
- [V2 迁移指南](https://docs.pydantic.dev/latest/migration/)
- [GitHub 仓库](https://github.com/pydantic/pydantic)

## ❓ 常见问题

**Q: 需要先学 V1 吗？**  
A: 不需要，直接学 V2 即可。

**Q: Python 版本要求？**  
A: Python 3.8+，推荐 3.10+。

**Q: 学完需要多久？**  
A: 建议用一整天（8-10小时）完整学习。

**Q: 如何检验学习效果？**  
A: 完成第7章实战练习，并在项目中应用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**开始学习吧！** 🎉

👉 [查看完整学习指南](learning/README_LEARNING.md)  
👉 [快速参考手册](learning/QUICK_REFERENCE.md)

# learn_pydantic_v2
