"""
安全相关功能
密码哈希、JWT token 生成和验证
"""
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# 密码哈希上下文
# bcrypt 是目前推荐的密码哈希算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码
    Returns:
        密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    生成密码哈希
    Args:
        password: 明文密码
    Returns:
        哈希后的密码
    """
    return pwd_context.hash(password)


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    """
    创建 JWT 访问令牌
    Args:
        user_id: 用户 ID
        expires_delta: 过期时间增量（可选）
    Returns:
        JWT token 字符串
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # JWT payload
    to_encode = {
        "exp": expire,  # 过期时间
        "sub": user_id,  # subject: 用户 ID
        "iat": datetime.now(timezone.utc),  # issued at: 签发时间
    }

    # 编码 JWT
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# 安全最佳实践：
# 1. 使用 bcrypt 哈希密码（不可逆）
# 2. 永远不要存储明文密码
# 3. JWT 使用 HS256 算法（对称加密）
# 4. Token 设置合理的过期时间
# 5. 使用强密钥（SECRET_KEY）
# 6. 在生产环境中使用环境变量存储密钥

