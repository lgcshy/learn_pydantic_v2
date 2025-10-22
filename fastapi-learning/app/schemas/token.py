"""
认证相关的 Pydantic Schemas
"""

from pydantic import BaseModel, Field


class Token(BaseModel):
    """JWT Token 响应"""

    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class TokenPayload(BaseModel):
    """JWT Token 载荷"""

    sub: int | None = None  # subject: 用户 ID
    exp: int | None = None  # expiration time: 过期时间


class LoginRequest(BaseModel):
    """
    登录请求（JSON 格式）

    现代主流的 JSON 登录方式
    """

    username: str = Field(
        ...,
        description="用户名或邮箱",
        examples=["testuser"],
    )
    password: str = Field(
        ...,
        description="密码",
        examples=["password123"],
    )
