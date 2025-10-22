# 快速开始指南

## 🚀 5 分钟快速启动

### 1. 安装依赖

```bash
cd fastapi-learning
uv sync
```

### 2. 创建测试用户

```bash
uv run python scripts/create_user.py
```

**测试账号：**
- 普通用户：`testuser` / `password123`
- 管理员：`admin` / `admin123`

### 3. 启动服务

```bash
# 方法 1：使用脚本
uv run python scripts/run.py

# 方法 2：直接运行
uv run python -m app.main

# 方法 3：使用 uvicorn
uv run uvicorn app.main:app --reload
```

服务启动后：
- 应用地址：http://localhost:8000
- API 文档：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc

### 4. 测试 API

#### 使用 Swagger UI（推荐）

1. 访问 http://localhost:8000/docs
2. 找到 `POST /api/v1/auth/login`
3. 点击 "Try it out"
4. 输入用户名和密码
5. 点击 "Execute"
6. 复制返回的 `access_token`
7. 点击页面顶部的 "Authorize" 按钮
8. 粘贴 token（格式：`Bearer <token>`）
9. 现在可以测试所有需要认证的 API

#### 使用 curl

```bash
# 1. 注册新用户
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "password123",
    "full_name": "New User"
  }'

# 2. 登录获取 token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"

# 3. 获取当前用户信息（需要 token）
TOKEN="your-access-token-here"
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# 4. 获取用户列表（需要管理员权限）
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer $TOKEN"
```

## 📚 学习路径

### 第一步：理解项目结构

阅读文档：
1. `docs/00_项目概览.md` - 了解整体架构
2. 浏览项目目录，熟悉文件组织

### 第二步：学习每一层

按顺序阅读：
1. `docs/01_Models层_SQLAlchemy.md` - 数据库层
2. `docs/02_Schemas层_Pydantic.md` - 数据验证层
3. `docs/03_CRUD层_业务逻辑.md` - 业务逻辑层
4. `docs/04_API层_FastAPI路由.md` - API 层
5. `docs/05_认证授权_JWT.md` - 认证授权

### 第三步：阅读源码

配合文档阅读源码：
1. `app/models/user.py` - 用户模型
2. `app/schemas/user.py` - 用户 Schemas
3. `app/crud/user.py` - 用户 CRUD
4. `app/api/v1/endpoints/users.py` - 用户 API
5. `app/core/security.py` - 安全相关

### 第四步：实战练习

尝试添加新功能：
1. 添加文章（Post）模型
2. 添加评论（Comment）模型
3. 实现文章的 CRUD API
4. 实现评论的嵌套关系
5. 添加标签（Tag）多对多关系

## 🎯 常用命令

```bash
# 启动服务（开发模式，自动重载）
uv run uvicorn app.main:app --reload

# 启动服务（指定端口）
uv run uvicorn app.main:app --reload --port 8080

# 启动服务（监听所有 IP）
uv run uvicorn app.main:app --reload --host 0.0.0.0

# 创建测试用户
uv run python scripts/create_user.py

# 测试配置加载
uv run python app/core/config.py

# 测试数据库连接
uv run python app/core/database.py
```

## 🔧 常见问题

### Q: 如何重置数据库？

```bash
rm -f app.db
uv run python scripts/create_user.py
```

### Q: 如何修改数据库？

1. 开发环境：删除 `app.db` 并重新运行
2. 生产环境：使用 Alembic 迁移

### Q: 如何添加新的端点？

1. 在 `app/api/v1/endpoints/` 创建新文件
2. 定义路由和处理函数
3. 在 `app/api/v1/api.py` 中注册路由

### Q: Token 过期怎么办？

重新登录获取新 token，或实现刷新 token 机制。

### Q: 如何切换到 PostgreSQL？

1. 修改 `.env` 中的 `DATABASE_URL`
2. 安装驱动：`uv add psycopg2-binary`
3. 重新运行应用

## 📖 下一步

- 阅读 README.md 了解项目详情
- 查看 docs/ 目录下的所有学习文档
- 尝试扩展项目功能
- 学习 Alembic 数据库迁移
- 添加单元测试

## 💡 学习建议

1. **边做边学**：启动项目后立即开始测试
2. **阅读源码**：理解每个文件的作用
3. **动手实践**：添加新功能巩固理解
4. **参考文档**：遇到问题查阅官方文档
5. **循序渐进**：不要急于求成，一步一步来

