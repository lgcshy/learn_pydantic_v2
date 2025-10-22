# API 层 - FastAPI 路由深入解析

## 🎯 API 层的职责

- 接收 HTTP 请求
- 验证请求数据（Pydantic）
- 调用 CRUD 层处理业务逻辑
- 返回格式化的响应
- 处理错误

## 📐 路由组织结构

### 分层路由

```
api/
└── v1/
    ├── api.py                 # 路由聚合
    ├── deps.py                # 依赖注入
    └── endpoints/
        ├── auth.py            # 认证相关
        ├── users.py           # 用户管理
        ├── posts.py           # 文章管理
        └── comments.py        # 评论管理
```

### 路由聚合

```python
# api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, posts

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(posts.router, prefix="/posts", tags=["文章"])
```

### 主应用注册

```python
# main.py
from app.api.v1.api import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
```

**最终路由：**

- `/api/v1/auth/login`
- `/api/v1/users/`
- `/api/v1/posts/`

## 🔧 路由装饰器详解

### 基本用法

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/")
def get_users():
    return [{"id": 1, "username": "john"}]
```

### HTTP 方法

```python
@router.get("/users/")        # 获取列表
@router.get("/users/{id}")    # 获取单个
@router.post("/users/")       # 创建
@router.put("/users/{id}")    # 完整更新
@router.patch("/users/{id}")  # 部分更新
@router.delete("/users/{id}") # 删除
```

### 路径参数

```python
@router.get("/users/{user_id}")
def get_user(user_id: int):  # 自动类型转换和验证
    return {"id": user_id}

# 枚举类型
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

@router.get("/users/role/{role}")
def get_users_by_role(role: UserRole):
    return {"role": role}
```

### 查询参数

```python
from typing import Annotated
from fastapi import Query

@router.get("/users/")
def get_users(
    # 可选参数
    skip: int = 0,
    limit: int = 10,
    
    # 必需参数
    q: str = Query(...),
    
    # 带验证的参数
    page: Annotated[int, Query(ge=1, le=1000)] = 1,
    
    # 多个值
    tags: Annotated[list[str], Query()] = None,
):
    return {"skip": skip, "limit": limit}
```

### 请求体

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str

@router.post("/users/")
def create_user(user: UserCreate):
    return user
```

### 响应模型

```python
@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # 返回的数据会被转换为 UserResponse
    return created_user

# 响应模型列表
@router.get("/users/", response_model=list[UserResponse])
def get_users():
    return users
```

### 状态码

```python
from fastapi import status

@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED  # 201 Created
)
def create_user(user: UserCreate):
    return created_user

@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT  # 204 No Content
)
def delete_user(user_id: int):
    user_crud.delete(db, id=user_id)
    return None
```

## 🎯 依赖注入详解

### 数据库会话依赖

```python
# deps.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 使用
from typing import Annotated
from fastapi import Depends

@router.get("/users/")
def get_users(db: Annotated[Session, Depends(get_db)]):
    return user_crud.get_multi(db)

# 简化写法（定义类型别名）
DBSession = Annotated[Session, Depends(get_db)]

@router.get("/users/")
def get_users(db: DBSession):
    return user_crud.get_multi(db)
```

### 当前用户依赖

```python
# deps.py
def get_current_user(
    db: DBSession,
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    # 验证 token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    
    # 获取用户
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    
    return user

# 使用
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/me")
def get_my_info(current_user: CurrentUser):
    return current_user
```

### 依赖链

```python
# 第一层：数据库
def get_db():
    ...

# 第二层：当前用户（依赖数据库）
def get_current_user(db: DBSession, token: str):
    ...

# 第三层：活跃用户（依赖当前用户）
def get_current_active_user(current_user: CurrentUser):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户已禁用")
    return current_user

# 第四层：管理员（依赖当前用户）
def get_current_superuser(current_user: CurrentUser):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    return current_user
```

## 🔐 认证端点实战

### 注册

```python
@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_in: UserCreate, db: DBSession):
    """用户注册"""
    # 检查邮箱是否已存在
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 检查用户名是否已存在
    user = user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="用户名已被使用")
    
    # 创建用户
    user = user_crud.create(db, obj_in=user_in)
    return user
```

### 登录方式对比

#### 方式 1：表单登录（OAuth2 标准，兼容 Swagger UI）

```python
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login", response_model=Token)
def login(
    db: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    用户登录（表单格式）
    
    优点：
    - 符合 OAuth2 标准
    - Swagger UI 自动支持（带 Authorize 按钮）
    
    缺点：
    - 使用 application/x-www-form-urlencoded
    - 不够现代，前端需要特殊处理
    """
    # 验证用户
    user = user_crud.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已禁用")
    
    # 创建 token
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")
```

#### 方式 2：JSON 登录（现代主流方式）⭐ 推荐

```python
from pydantic import BaseModel

class LoginRequest(BaseModel):
    """登录请求（JSON 格式）"""
    username: str
    password: str

@router.post("/login/json", response_model=Token)
def login_json(
    login_data: LoginRequest,
    db: DBSession,
):
    """
    用户登录（JSON 格式）
    
    优点：
    - 使用 application/json（现代标准）
    - 前端友好，直接发送 JSON
    - 更灵活，可以轻松扩展字段
    
    请求示例：
    ```json
    {
        "username": "testuser",
        "password": "password123"
    }
    ```
    
    响应示例：
    ```json
    {
        "access_token": "eyJhbGc...",
        "token_type": "bearer"
    }
    ```
    """
    # 验证用户
    user = user_crud.authenticate(
        db, username=login_data.username, password=login_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已禁用")
    
    # 创建 token
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")
```

#### Token 使用方式（请求头）

登录成功后，客户端需要在后续请求中携带 token：

```http
GET /api/v1/users/me HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

FastAPI 自动处理：

```python
from fastapi.security import OAuth2PasswordBearer

# 自动从 Authorization: Bearer {token} 中提取 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(
    db: DBSession,
    token: Annotated[str, Depends(oauth2_scheme)]  # 自动从请求头获取
) -> User:
    """
    从 Authorization header 验证用户
    
    客户端请求头：
    Authorization: Bearer <token>
    
    工作流程：
    1. FastAPI 自动从请求头中提取 Authorization 字段
    2. 解析 "Bearer <token>" 格式，提取 token 部分
    3. 将 token 传递给此函数进行验证
    4. 解码 JWT token 获取用户 ID
    5. 从数据库查询用户信息
    6. 返回用户对象或抛出异常
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效的认证凭据")
    except JWTError:
        raise HTTPException(status_code=401, detail="无效的认证凭据")
    
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    
    return user
```

#### Token 提取机制详解

**1. 请求头格式**
```http
GET /api/v1/users/me HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**2. OAuth2PasswordBearer 自动处理**
```python
# FastAPI 内部处理流程（简化版）
def extract_token_from_header(authorization: str) -> str:
    """
    OAuth2PasswordBearer 内部实现逻辑
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供认证信息")
    
    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="认证方案必须是 Bearer")
    
    return token
```

**3. 依赖注入链**
```python
# 依赖链：请求 → OAuth2PasswordBearer → get_current_user → 端点函数
@router.get("/me")
def get_current_user_info(
    current_user: CurrentUser  # 依赖链：db → token → user
):
    return current_user
```

**4. 错误处理**
```python
# 各种认证失败情况
try:
    # 1. 没有 Authorization 头
    # → HTTP 401: "Not authenticated"
    
    # 2. Authorization 头格式错误
    # → HTTP 401: "Invalid authentication scheme"
    
    # 3. Token 无效或过期
    # → HTTP 401: "Could not validate credentials"
    
    # 4. 用户不存在
    # → HTTP 401: "User not found"
    
except Exception as e:
    raise HTTPException(status_code=401, detail=str(e))
```

#### 前端调用示例

**方式 1：表单登录（需要特殊处理）**

```javascript
// 不推荐：需要转换为表单格式
const formData = new URLSearchParams();
formData.append('username', 'testuser');
formData.append('password', 'password123');

const response = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: formData,
});

const data = await response.json();
// { "access_token": "eyJ...", "token_type": "bearer" }
```

**方式 2：JSON 登录（推荐）** ⭐

```javascript
// 推荐：直接发送 JSON
const response = await fetch('/api/v1/auth/login/json', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'testuser',
    password: 'password123',
  }),
});

const data = await response.json();
const token = data.access_token;

// 保存 token
localStorage.setItem('token', token);
```

**使用 Token 访问受保护的接口：**

```javascript
const token = localStorage.getItem('token');

const response = await fetch('/api/v1/users/me', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,  // 关键：Bearer + 空格 + token
  },
});

const user = await response.json();
```

#### Token 在请求头中的完整流程

**1. 客户端发送请求**
```javascript
// 前端代码
const token = localStorage.getItem('token');

fetch('/api/v1/users/me', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,  // 关键：Bearer + 空格 + token
    'Content-Type': 'application/json',
  },
})
.then(response => response.json())
.then(data => console.log(data));
```

**2. HTTP 请求格式**
```http
GET /api/v1/users/me HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsImV4cCI6MTYz...
Content-Type: application/json
```

**3. FastAPI 自动提取**
```python
# FastAPI 内部处理（OAuth2PasswordBearer）
def extract_token(request: Request) -> str:
    """
    FastAPI 自动从请求头提取 token
    """
    authorization = request.headers.get("Authorization")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    return token
```

**4. 依赖注入传递**
```python
# 依赖链：OAuth2PasswordBearer → get_current_user → 端点函数
@router.get("/me")
def get_current_user_info(
    current_user: CurrentUser  # 内部流程：
    # 1. OAuth2PasswordBearer 提取 token
    # 2. get_current_user 验证 token
    # 3. 返回用户对象
):
    return current_user
```

**5. 错误响应**
```json
// 认证失败时的响应
{
  "detail": "Could not validate credentials"
}
```

#### 对比总结

| 特性 | 表单登录 (OAuth2) | JSON 登录 (现代) |
|------|------------------|-----------------|
| Content-Type | `application/x-www-form-urlencoded` | `application/json` |
| 请求格式 | `username=xxx&password=xxx` | `{"username":"xxx","password":"xxx"}` |
| Swagger UI 支持 | ✅ 自动集成 Authorize 按钮 | ⚠️ 需要手动输入 token |
| 前端友好度 | ⭐⭐ 需要转换格式 | ⭐⭐⭐⭐⭐ 直接发送对象 |
| 扩展性 | ⭐⭐ 受限于表单格式 | ⭐⭐⭐⭐⭐ 灵活添加字段 |
| 标准符合 | OAuth2 标准 | RESTful API 常规做法 |
| **推荐场景** | 快速开发、测试 | **生产环境、前后端分离** |

**最佳实践：**

- 🔧 开发测试：提供表单登录（方便 Swagger UI 测试）
- 🚀 生产环境：使用 JSON 登录（现代、前端友好）
- 💡 建议：**同时提供两个端点**，让开发者自由选择

### 获取当前用户信息

```python
@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: CurrentUser):
    """获取当前登录用户信息"""
    return current_user
```

## 📊 CRUD 端点实战

### 列表（分页）

```python
@router.get("/", response_model=UserListResponse)
def get_users(
    db: DBSession,
    current_user: CurrentSuperUser,  # 需要管理员权限
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """获取用户列表（分页）"""
    skip = (page - 1) * page_size
    users = user_crud.get_multi(db, skip=skip, limit=page_size)
    total = user_crud.get_count(db)
    
    return UserListResponse(
        total=total,
        items=users,
        page=page,
        page_size=page_size,
    )
```

### 详情

```python
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    """获取用户详情"""
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 权限检查：非管理员只能查看自己
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return user
```

### 创建

```python
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_in: UserCreate,
    db: DBSession,
    current_user: CurrentSuperUser,  # 需要管理员权限
):
    """创建用户"""
    # 验证唯一性
    if user_crud.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="邮箱已被使用")
    
    if user_crud.get_by_username(db, username=user_in.username):
        raise HTTPException(status_code=400, detail="用户名已被使用")
    
    user = user_crud.create(db, obj_in=user_in)
    return user
```

### 更新

```python
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: DBSession,
    current_user: CurrentUser,
):
    """更新用户"""
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 权限检查
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 验证唯一性
    if user_in.email and user_in.email != user.email:
        if user_crud.get_by_email(db, email=user_in.email):
            raise HTTPException(status_code=400, detail="邮箱已被使用")
    
    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return user
```

### 删除

```python
@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    db: DBSession,
    current_user: CurrentSuperUser,
):
    """删除用户"""
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 不能删除自己
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    user_crud.delete(db, id=user_id)
```

## ⚠️ 错误处理

### HTTPException

```python
from fastapi import HTTPException, status

# 404 Not Found
raise HTTPException(status_code=404, detail="资源不存在")

# 400 Bad Request
raise HTTPException(status_code=400, detail="请求参数错误")

# 401 Unauthorized
raise HTTPException(
    status_code=401,
    detail="未认证",
    headers={"WWW-Authenticate": "Bearer"},
)

# 403 Forbidden
raise HTTPException(status_code=403, detail="权限不足")

# 使用状态码常量
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="用户不存在"
)
```

### 全局异常处理

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
```

## 📝 文档优化

### 添加描述和示例

```python
@router.post(
    "/users/",
    response_model=UserResponse,
    status_code=201,
    summary="创建用户",
    description="创建一个新用户，需要提供用户名、邮箱和密码",
    response_description="返回创建的用户信息",
)
def create_user(
    user_in: UserCreate,
    db: DBSession,
):
    """
    创建新用户：
    
    - **email**: 用户邮箱（必需）
    - **username**: 用户名（必需，3-50字符）
    - **password**: 密码（必需，至少8字符）
    - **full_name**: 全名（可选）
    """
    return user_crud.create(db, obj_in=user_in)
```

### Tags 分组

```python
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证"],  # Swagger UI 中的分组
)
```

## 🎯 最佳实践

1. **使用类型提示**
   - 所有参数都要有类型提示
   - 使用 `Annotated` 组合依赖

2. **明确响应模型**
   - 使用 `response_model` 控制响应格式
   - 不要返回敏感信息

3. **合适的状态码**
   - 201: 创建成功
   - 204: 删除成功
   - 400: 请求错误
   - 401: 未认证
   - 403: 权限不足
   - 404: 资源不存在

4. **权限检查**
   - 使用依赖注入进行权限检查
   - 在端点中进行业务级权限验证

5. **错误信息友好**
   - 提供清晰的错误描述
   - 中文错误信息更友好

## 📚 参考资料

- [FastAPI 路由](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [依赖注入](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [安全认证](https://fastapi.tiangolo.com/tutorial/security/)

