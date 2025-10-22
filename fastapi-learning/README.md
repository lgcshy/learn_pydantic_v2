# FastAPI + SQLAlchemy + Pydantic 学习项目

一个完整的 FastAPI 学习项目，展示了如何使用 FastAPI、SQLAlchemy 和 Pydantic 构建现代 Web API。

## 📚 项目特性

- ✅ 标准的项目结构（三层架构）
- ✅ SQLAlchemy 2.0 ORM
- ✅ Pydantic V2 数据验证
- ✅ JWT 认证和授权
- ✅ 密码哈希（bcrypt）
- ✅ 依赖注入
- ✅ CORS 配置
- ✅ 完整的类型提示
- ✅ RESTful API 设计
- ✅ 自动 API 文档（Swagger UI / ReDoc）

## 🏗️ 项目结构

```
fastapi-learning/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/        # API 端点
│   │       │   ├── auth.py       # 认证相关
│   │       │   └── users.py      # 用户管理
│   │       ├── api.py            # 路由聚合
│   │       └── deps.py           # 依赖注入
│   ├── core/
│   │   ├── config.py             # 配置管理
│   │   ├── database.py           # 数据库连接
│   │   └── security.py           # 安全功能
│   ├── crud/
│   │   ├── base.py               # 通用 CRUD 基类
│   │   └── user.py               # 用户 CRUD
│   ├── models/
│   │   └── user.py               # SQLAlchemy 模型
│   ├── schemas/
│   │   ├── token.py              # Token Schemas
│   │   └── user.py               # 用户 Schemas
│   └── main.py                   # 应用入口
├── docs/                         # 学习文档
├── scripts/                      # 工具脚本
├── .env                          # 环境变量
├── .gitignore
├── pyproject.toml                # 项目依赖
└── README.md
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 2. 配置环境变量

复制 `.env.example` 到 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 3. 运行应用

```bash
# 方法 1: 直接运行
python -m app.main

# 方法 2: 使用 uvicorn
uvicorn app.main:app --reload

# 方法 3: 使用脚本
python scripts/run.py
```

### 4. 创建初始用户

```bash
python scripts/create_user.py
```

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📖 API 端点

### 认证

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户信息
- `POST /api/v1/auth/test-token` - 测试 token

### 用户管理

- `GET /api/v1/users/` - 获取用户列表（需要管理员）
- `GET /api/v1/users/{user_id}` - 获取用户详情
- `PUT /api/v1/users/{user_id}` - 更新用户
- `DELETE /api/v1/users/{user_id}` - 删除用户（需要管理员）

## 🧪 测试 API

### 1. 注册用户

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### 2. 登录获取 token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  -d "username=testuser&password=password123"
```

### 3. 使用 token 访问受保护端点

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \\
  -H "Authorization: Bearer <your-token>"
```

## 🎯 学习重点

### 1. 项目结构（三层架构）

- **Models 层**：SQLAlchemy 模型，定义数据库表结构
- **Schemas 层**：Pydantic 模型，定义 API 输入输出
- **CRUD 层**：数据库操作逻辑
- **API 层**：路由和端点定义

### 2. Pydantic V2 特性

- `model_config = ConfigDict(from_attributes=True)` - 从 ORM 对象创建
- `model_dump(exclude_unset=True)` - 导出数据（只包含设置的字段）
- `Field()` - 字段验证和文档
- 类型提示和验证

### 3. SQLAlchemy 2.0 风格

- `Mapped` 和 `mapped_column` - 类型化的列定义
- `select()` API - 现代查询语法
- 声明式基类 `DeclarativeBase`

### 4. FastAPI 依赖注入

- `Depends()` - 依赖注入
- 依赖链 - 多层依赖
- 全局依赖 - 应用级依赖

### 5. JWT 认证流程

1. 用户登录 → 验证密码
2. 生成 JWT token
3. 客户端存储 token
4. 请求时携带 token
5. 服务端验证 token

## 🔧 核心概念

### Models vs Schemas

```python
# SQLAlchemy Model (数据库层)
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)

# Pydantic Schema (API 层)
class UserResponse(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)
```

### CRUD 模式

```python
# 创建
user = user_crud.create(db, obj_in=user_create)

# 读取
user = user_crud.get(db, id=1)
users = user_crud.get_multi(db, skip=0, limit=10)

# 更新
user = user_crud.update(db, db_obj=user, obj_in=user_update)

# 删除
user_crud.delete(db, id=1)
```

### 依赖注入

```python
# 数据库会话依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 使用依赖
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return user_crud.get_multi(db)
```

## 📝 最佳实践

1. **分离关注点**：Models、Schemas、CRUD 分层清晰
2. **类型提示**：充分使用 Python 类型系统
3. **依赖注入**：复用逻辑，提高可测试性
4. **错误处理**：使用 HTTPException 返回友好错误
5. **安全**：密码哈希、JWT 验证、权限检查
6. **文档**：使用 docstrings 和 Field 描述

## 🎓 学习资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic V2 文档](https://docs.pydantic.dev/latest/)
- [SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/)

## 📄 许可证

MIT License

