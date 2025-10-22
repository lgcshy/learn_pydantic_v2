"""
认证相关的 API 端点
登录、注册等功能
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.deps import CurrentUser, DBSession
from app.core.config import settings
from app.core.security import create_access_token
from app.crud.user import user_crud
from app.schemas.token import LoginRequest, Token
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: DBSession) -> UserResponse:
    """
    用户注册
    """
    # 检查邮箱是否已存在
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )

    # 检查用户名是否已存在
    user = user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用",
        )

    # 创建用户
    user = user_crud.create(db, obj_in=user_in)
    return user


@router.post("/login", response_model=Token)
def login(db: DBSession, form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    用户登录（OAuth2 表单格式）

    使用 application/x-www-form-urlencoded 格式

    优点：
    - 符合 OAuth2 标准
    - Swagger UI 自动支持（Authorize 按钮）

    缺点：
    - 需要表单格式，不够现代

    **推荐使用 /login/json 端点进行 JSON 登录**
    """
    # 验证用户
    user = user_crud.authenticate(db, username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账号已被禁用",
        )

    # 创建 access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.post("/login/json", response_model=Token)
def login_json(login_data: LoginRequest, db: DBSession) -> Token:
    """
    用户登录（JSON 格式）⭐ 推荐

    使用 application/json 格式（现代主流方式）

    优点：
    - 前端友好，直接发送 JSON 对象
    - 更灵活，易于扩展字段
    - 符合 RESTful API 标准

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
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
    ```

    使用 token：
    在后续请求的 Header 中添加：
    ```
    Authorization: Bearer {access_token}
    ```
    """
    # 验证用户
    user = user_crud.authenticate(db, username=login_data.username, password=login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户账号已被禁用",
        )

    # 创建 access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: CurrentUser) -> UserResponse:
    """
    获取当前登录用户信息
    需要认证
    """
    return current_user


@router.post("/test-token", response_model=UserResponse)
def test_token(current_user: CurrentUser) -> UserResponse:
    """
    测试 token 是否有效
    需要认证
    """
    return current_user
