"""
API 依赖注入函数
集中管理所有可复用的依赖项
"""
from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.token import TokenPayload

# OAuth2 密码流（用于 JWT 认证）
# tokenUrl 是获取 token 的端点路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# 类型别名，用于简化依赖注入的类型标注
DBSession = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(db: DBSession, token: TokenDep) -> User:
    """
    获取当前登录用户的依赖函数
    从 JWT token 中解析用户信息并验证
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 解码 JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int | None = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        token_data = TokenPayload(sub=user_id)
    except JWTError:
        raise credentials_exception

    # 从数据库获取用户
    user = user_crud.get(db, id=token_data.sub)
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    获取当前活跃用户（未禁用）
    这是一个依赖链的示例：依赖于 get_current_user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户账号已被禁用")
    return current_user


def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    获取当前超级用户
    用于需要管理员权限的端点
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="权限不足，需要管理员权限")
    return current_user


# 类型别名，用于简化控制器中的类型标注
CurrentUser = Annotated[User, Depends(get_current_active_user)]
CurrentSuperUser = Annotated[User, Depends(get_current_superuser)]

