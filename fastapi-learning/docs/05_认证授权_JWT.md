# 认证授权 - JWT 深入解析

## 🎯 认证 vs 授权

- **认证 (Authentication)**：验证用户是谁（登录）
- **授权 (Authorization)**：验证用户能做什么（权限）

## 🔐 JWT 工作原理

### JWT 是什么？

**JWT (JSON Web Token)** - 一种用于在网络应用间传递信息的token格式

### JWT 结构

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNjQwMDAwMDAwfQ.signature

Header.Payload.Signature
```

**1. Header（头部）**

```json
{
  "alg": "HS256",  // 算法
  "typ": "JWT"     // 类型
}
```

**2. Payload（载荷）**

```json
{
  "sub": "1",           // subject: 用户 ID
  "exp": 1640000000,    // expiration: 过期时间
  "iat": 1639900000     // issued at: 签发时间
}
```

**3. Signature（签名）**
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

### JWT 优点

✅ 无状态 - 服务器不需要存储 session
✅ 可扩展 - 可以添加自定义字段
✅ 跨域 - 可以用于不同域名
✅ 性能好 - 不需要查询数据库验证

### JWT 缺点

❌ 无法主动失效 - token 未过期前一直有效
❌ 大小较大 - 比 session ID 大
❌ 密钥泄露风险 - 需要妥善保管

## 🔧 实现 JWT 认证

### 1. 安装依赖

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

### 2. 配置

```python
# core/config.py
class Settings(BaseSettings):
    SECRET_KEY: str  # 密钥（必须保密！）
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

### 3. 密码哈希

```python
# core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)
```

**为什么使用 bcrypt？**

- 单向哈希（不可逆）
- 自动加盐
- 计算成本可调
- 行业标准

### 4. 创建 Token

```python
# core/security.py
from datetime import datetime, timedelta, timezone
from jose import jwt

def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    """创建 JWT access token"""
    # 设置过期时间
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # 构建 payload
    to_encode = {
        "exp": expire,              # 过期时间
        "sub": user_id,             # 用户 ID
        "iat": datetime.now(timezone.utc),  # 签发时间
    }
    
    # 编码 JWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
```

### 5. 验证 Token

```python
# api/v1/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# OAuth2 密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    db: DBSession,
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """获取当前登录用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 解码 JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int | None = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # 从数据库获取用户
    user = user_crud.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    
    return user
```

## 🔑 完整认证流程

### 1. 注册

```python
@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_in: UserCreate, db: DBSession):
    """用户注册"""
    # 检查用户是否存在
    if user_crud.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="邮箱已注册")
    
    # 创建用户（密码会被自动哈希）
    user = user_crud.create(db, obj_in=user_in)
    return user
```

### 2. 登录

```python
@router.post("/login", response_model=Token)
def login(
    db: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """用户登录"""
    # 验证用户名和密码
    user = user_crud.authenticate(
        db,
        username=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    
    # 创建 token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.id,
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
```

### 3. 访问受保护端点

```python
@router.get("/me", response_model=UserResponse)
def get_my_info(current_user: CurrentUser):
    """获取当前用户信息（需要登录）"""
    return current_user
```

### 4. 客户端使用流程

```bash
# 1. 登录获取 token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"

# 响应
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}

# 2. 使用 token 访问受保护端点
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGci..."
```

## 🛡️ 权限控制

### 基于角色的访问控制 (RBAC)

#### 1. 数据库模型

```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
```

#### 2. 权限依赖

```python
# api/v1/deps.py

def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return current_user

def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """获取当前管理员用户"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    return current_user

# 类型别名
CurrentUser = Annotated[User, Depends(get_current_active_user)]
CurrentSuperUser = Annotated[User, Depends(get_current_superuser)]
```

#### 3. 使用权限

```python
# 普通用户可访问
@router.get("/me")
def get_my_info(current_user: CurrentUser):
    return current_user

# 仅管理员可访问
@router.get("/users/")
def get_all_users(current_user: CurrentSuperUser, db: DBSession):
    return user_crud.get_multi(db)

# 业务级权限检查
@router.get("/users/{user_id}")
def get_user(user_id: int, current_user: CurrentUser, db: DBSession):
    user = user_crud.get(db, id=user_id)
    
    # 非管理员只能查看自己
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return user
```

## 🔒 安全最佳实践

### 1. 密钥安全

```python
# ❌ 不要硬编码密钥
SECRET_KEY = "my-secret-key"

# ✅ 使用环境变量
SECRET_KEY = os.getenv("SECRET_KEY")

# ✅ 生成强密钥
import secrets
secret_key = secrets.token_urlsafe(32)
```

### 2. HTTPS

```python
# 生产环境必须使用 HTTPS
# HTTP 会暴露 token

# 在配置中强制 HTTPS
if not settings.DEBUG:
    assert request.url.scheme == "https"
```

### 3. Token 过期时间

```python
# 短期 token（推荐）
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30分钟

# 刷新 token（可选）
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7天
```

### 4. 密码策略

```python
@field_validator('password')
@classmethod
def password_strength(cls, v: str) -> str:
    if len(v) < 8:
        raise ValueError('密码至少8位')
    if not any(c.isupper() for c in v):
        raise ValueError('密码必须包含大写字母')
    if not any(c.islower() for c in v):
        raise ValueError('密码必须包含小写字母')
    if not any(c.isdigit() for c in v):
        raise ValueError('密码必须包含数字')
    return v
```

### 5. 速率限制

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # 每分钟最多5次
async def login(request: Request):
    ...
```

## 🎯 常见问题

### Q: Token 如何失效？

A: JWT 无法主动失效，解决方案：

1. 设置短期过期时间
2. 使用刷新 token
3. 维护黑名单（需要存储）

### Q: 如何存储 Token？

```javascript
// ✅ 推荐：localStorage
localStorage.setItem('access_token', token);

// ❌ 不推荐：Cookie（CSRF 风险）
// 除非使用 httpOnly + SameSite
```

### Q: 如何刷新 Token？

```python
# 实现刷新 token 端点
@router.post("/refresh")
def refresh_token(current_user: CurrentUser):
    new_token = create_access_token(current_user.id)
    return Token(access_token=new_token, token_type="bearer")
```

## 📊 完整示例

```python
# 完整的认证流程
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_in: UserCreate, db: DBSession):
    if user_crud.get_by_email(db, email=user_in.email):
        raise HTTPException(status_code=400, detail="邮箱已注册")
    user = user_crud.create(db, obj_in=user_in)
    return user

@router.post("/login", response_model=Token)
def login(
    db: DBSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = user_crud.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="认证失败")
    
    access_token = create_access_token(
        user.id,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser):
    return current_user
```

## 📚 参考资料

- [JWT 官网](https://jwt.io/)
- [FastAPI 安全](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth2 规范](https://oauth.net/2/)

