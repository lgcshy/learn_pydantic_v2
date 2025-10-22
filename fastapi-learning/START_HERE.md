# �� 从这里开始

## 欢迎来到 FastAPI 学习项目！

这是一个**完整的、生产级别的** FastAPI 学习项目。包含：
- ✅ 完整的用户认证系统（JWT）
- ✅ RESTful API 设计
- ✅ 三层架构实现
- ✅ 详细的学习文档（15,000+ 字）
- ✅ 测试账号和数据

## 🎯 第一步：启动项目（5分钟）

### 1. 确认依赖已安装

```bash
cd /home/lgc/workspace/python/pydantic-v2/fastapi-learning
uv sync
```

### 2. 启动服务

```bash
uv run python scripts/run.py
```

或者：

```bash
uv run uvicorn app.main:app --reload
```

### 3. 访问 API 文档

打开浏览器访问：
- **Swagger UI**: http://localhost:8000/docs ⭐ 强烈推荐
- **ReDoc**: http://localhost:8000/redoc

## 🔑 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| testuser | password123 | 普通用户 |
| admin | admin123 | 管理员 |

## 📝 如何测试 API（Swagger UI）

1. 访问 http://localhost:8000/docs
2. 找到 `POST /api/v1/auth/login`
3. 点击 "Try it out"
4. 输入 `username: admin` 和 `password: admin123`
5. 点击 "Execute"
6. 复制返回的 `access_token`
7. 点击页面顶部的 **🔓 Authorize** 按钮
8. 粘贴 token
9. 现在可以测试所有需要认证的 API 了！

## 📚 第二步：学习文档（按顺序）

### 快速了解
1. **[QUICK_START.md](QUICK_START.md)** - 5分钟快速开始
2. **[README.md](README.md)** - 项目详细说明

### 系统学习（推荐按此顺序）
1. **[docs/INDEX.md](docs/INDEX.md)** - 文档导航
2. **[docs/00_项目概览.md](docs/00_项目概览.md)** - 架构设计
3. **[docs/01_Models层_SQLAlchemy.md](docs/01_Models层_SQLAlchemy.md)** - 数据库层
4. **[docs/02_Schemas层_Pydantic.md](docs/02_Schemas层_Pydantic.md)** - 数据验证
5. **[docs/03_CRUD层_业务逻辑.md](docs/03_CRUD层_业务逻辑.md)** - 业务逻辑
6. **[docs/04_API层_FastAPI路由.md](docs/04_API层_FastAPI路由.md)** - API 开发
7. **[docs/05_认证授权_JWT.md](docs/05_认证授权_JWT.md)** - 认证系统

### 总结回顾
- **[docs/学习总结.md](docs/学习总结.md)** - 知识总结
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - 项目总结

## 🎯 学习建议

### 上午（3-4小时）
1. 启动项目，测试 API（30分钟）
2. 阅读项目概览（30分钟）
3. 学习 Models 层（1小时）
4. 学习 Schemas 层（1小时）

### 下午（3-4小时）
5. 学习 CRUD 层（1.5小时）
6. 学习 API 层（1.5小时）
7. 学习认证授权（1小时）

### 晚上（2小时）
8. 通读学习总结
9. 实战练习：添加新功能

## 💡 核心知识点

### 三层架构
```
用户请求 → API层 → CRUD层 → Models层 → 数据库
           ↓        ↓         ↓
        FastAPI   业务逻辑   SQLAlchemy
           ↑
       Pydantic
```

### 项目结构
```
app/
├── api/v1/endpoints/  # 📍 从这里开始看 API 实现
├── schemas/           # 📍 看数据验证
├── crud/              # 📍 看业务逻辑
├── models/            # 📍 看数据库表定义
└── core/              # 📍 看核心配置
```

## 🚀 实战练习

### 任务：添加文章（Post）功能

1. **创建模型** `app/models/post.py`
2. **创建 Schema** `app/schemas/post.py`
3. **创建 CRUD** `app/crud/post.py`
4. **创建 API** `app/api/v1/endpoints/posts.py`
5. **注册路由** 在 `app/api/v1/api.py`

参考用户模块的实现方式！

## ❓ 常见问题

**Q: 如何重置数据库？**
```bash
rm -f app.db
uv run python scripts/create_user.py
```

**Q: 如何查看 SQL 日志？**
在 `.env` 中设置 `DEBUG=True`

**Q: Token 过期了怎么办？**
重新登录获取新 token

**Q: 如何添加新的 API 端点？**
参考 `app/api/v1/endpoints/users.py`

## 🎉 开始学习吧！

一切准备就绪，开始你的 FastAPI 学习之旅吧！

**记住：边做边学，动手实践最重要！** 💪

有问题？查看文档或阅读源码中的注释。

祝学习顺利！��
