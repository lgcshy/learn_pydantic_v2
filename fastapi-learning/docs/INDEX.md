# FastAPI 学习文档索引

## 📚 文档导航

### 🚀 快速开始

- [QUICK_START.md](../QUICK_START.md) - 5分钟快速启动指南
- [README.md](../README.md) - 项目详细介绍

### 📖 核心概念（按学习顺序）

1. **[00_项目概览.md](00_项目概览.md)**
   - 项目架构
   - 三层设计
   - 核心概念
   - 数据流

2. **[01_Models层_SQLAlchemy.md](01_Models层_SQLAlchemy.md)**
   - ORM 基础
   - SQLAlchemy 2.0 新特性
   - 模型定义
   - 字段类型
   - 关系处理

3. **[02_Schemas层_Pydantic.md](02_Schemas层_Pydantic.md)**
   - Pydantic V2 核心特性
   - Schema 设计模式
   - 数据验证
   - 字段类型
   - 序列化

4. **[03_CRUD层_业务逻辑.md](03_CRUD层_业务逻辑.md)**
   - CRUD 模式
   - 通用基类
   - 查询操作
   - 事务处理
   - 高级查询

5. **[04_API层_FastAPI路由.md](04_API层_FastAPI路由.md)**
   - 路由定义
   - 依赖注入
   - 请求处理
   - 响应格式
   - 错误处理

6. **[05_认证授权_JWT.md](05_认证授权_JWT.md)**
   - JWT 原理
   - 认证流程
   - 权限控制
   - 安全最佳实践

### 📝 总结文档

- **[学习总结.md](学习总结.md)**
  - 核心知识点总结
  - 最佳实践清单
  - 进阶学习方向
  - 学习资源

## 🎯 推荐学习路径

### 新手路径（第一天）

**上午（9:00-12:00）：基础架构**
1. 阅读 `QUICK_START.md`，快速启动项目
2. 阅读 `00_项目概览.md`，理解整体架构
3. 阅读 `01_Models层_SQLAlchemy.md`，学习数据库层
4. 查看 `app/models/user.py` 源码

**下午（14:00-18:00）：数据和业务逻辑**
5. 阅读 `02_Schemas层_Pydantic.md`，学习数据验证
6. 查看 `app/schemas/user.py` 源码
7. 阅读 `03_CRUD层_业务逻辑.md`，学习业务逻辑
8. 查看 `app/crud/user.py` 和 `app/crud/base.py` 源码

**晚上（19:00-21:00）：API 和认证**
9. 阅读 `04_API层_FastAPI路由.md`，学习 API 开发
10. 查看 `app/api/v1/endpoints/` 下的源码
11. 阅读 `05_认证授权_JWT.md`，学习认证授权
12. 通过 Swagger UI 测试所有 API

### 进阶路径（第二天）

**实战练习**
1. 添加 Post（文章）模型
2. 实现文章的 CRUD 操作
3. 添加 Comment（评论）模型
4. 实现用户、文章、评论的关联
5. 添加标签系统（多对多关系）
6. 实现搜索和过滤功能
7. 添加分页功能
8. 编写单元测试

## 📂 项目结构速查

```
fastapi-learning/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/      # 📍 API 端点实现
│   │   ├── api.py          # 📍 路由聚合
│   │   └── deps.py         # 📍 依赖注入
│   ├── core/
│   │   ├── config.py       # 📍 配置管理
│   │   ├── database.py     # 📍 数据库连接
│   │   └── security.py     # 📍 安全功能
│   ├── crud/
│   │   ├── base.py         # 📍 通用 CRUD 基类
│   │   └── user.py         # 📍 用户 CRUD
│   ├── models/
│   │   └── user.py         # 📍 用户模型
│   ├── schemas/
│   │   ├── token.py        # 📍 Token Schemas
│   │   └── user.py         # 📍 用户 Schemas
│   └── main.py             # 📍 应用入口
├── docs/                   # 📚 学习文档
├── scripts/                # 🔧 工具脚本
├── .env                    # ⚙️ 环境配置
├── pyproject.toml          # 📦 项目依赖
├── QUICK_START.md          # 🚀 快速开始
└── README.md               # 📖 项目说明
```

## 🎓 学习技巧

### 1. 边做边学

- 不要只看文档，要动手实践
- 每读完一个文档，就查看对应的源码
- 修改代码，观察变化

### 2. 使用 Swagger UI

- 启动应用后访问 http://localhost:8000/docs
- 这是最好的 API 测试工具
- 可以看到所有端点和数据结构

### 3. 阅读错误信息

- FastAPI 的错误信息非常详细
- Pydantic 的验证错误很清晰
- 学会从错误中学习

### 4. 查看日志

- SQLAlchemy 会打印执行的 SQL
- 有助于理解 ORM 的工作原理
- 在 `config.py` 中设置 `DEBUG=True`

### 5. 使用类型提示

- 充分利用 IDE 的自动补全
- 类型错误会在编写时提示
- 提高开发效率

## 🔖 常用链接

### 项目相关

- API 文档：http://localhost:8000/docs
- ReDoc：http://localhost:8000/redoc
- OpenAPI Schema：http://localhost:8000/openapi.json

### 官方文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Pydantic V2 文档](https://docs.pydantic.dev/latest/)
- [SQLAlchemy 2.0 文档](https://docs.sqlalchemy.org/en/20/)
- [Uvicorn 文档](https://www.uvicorn.org/)

### 学习资源

- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [FastAPI 教程](https://fastapi.tiangolo.com/tutorial/)
- [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi)

## ❓ 常见问题

### Q: 文档应该按什么顺序阅读？

A: 按编号顺序：00 → 01 → 02 → 03 → 04 → 05

### Q: 源码应该如何阅读？

A: 建议顺序：

1. `app/models/user.py`
2. `app/schemas/user.py`
3. `app/crud/base.py`
4. `app/crud/user.py`
5. `app/api/v1/deps.py`
6. `app/api/v1/endpoints/auth.py`
7. `app/api/v1/endpoints/users.py`

### Q: 如何快速上手？

A: 

1. 看 `QUICK_START.md`（5分钟）
2. 启动项目，测试 API（10分钟）
3. 阅读 `00_项目概览.md`（15分钟）
4. 开始逐层学习

### Q: 遇到问题怎么办？

A:

1. 查看错误信息
2. 检查日志输出
3. 阅读相关文档
4. 查看源码注释
5. 搜索官方文档

## 📝 学习检查清单

完成以下任务，确保掌握核心知识：

### 基础知识

- [ ] 理解三层架构的设计理念
- [ ] 掌握 SQLAlchemy 模型定义
- [ ] 理解 Pydantic Schema 的作用
- [ ] 掌握 CRUD 操作的实现
- [ ] 理解依赖注入的概念
- [ ] 掌握 JWT 认证流程

### 实践能力

- [ ] 能创建新的模型
- [ ] 能定义对应的 Schemas
- [ ] 能实现 CRUD 操作
- [ ] 能创建新的 API 端点
- [ ] 能处理错误和异常
- [ ] 能实现权限控制

### 进阶技能

- [ ] 理解一对多关系
- [ ] 理解多对多关系
- [ ] 能实现复杂查询
- [ ] 能优化数据库查询
- [ ] 能编写单元测试
- [ ] 能部署到生产环境

## 🎉 开始学习

准备好了吗？从 [QUICK_START.md](../QUICK_START.md) 开始你的 FastAPI 学习之旅吧！

