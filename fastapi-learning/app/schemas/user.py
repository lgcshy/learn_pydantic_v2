"""
用户 Pydantic Schemas（API 层）
定义请求和响应的数据结构
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_serializer

from app.core.config import settings


# ========== 基础 Schema ==========
class UserBase(BaseModel):
    """用户基础字段（共享字段）"""

    email: EmailStr = Field(..., description="用户邮箱", examples=["user@example.com"])
    username: str = Field(
        ..., min_length=3, max_length=50, description="用户名", examples=["johndoe"]
    )
    full_name: str | None = Field(None, max_length=100, description="全名", examples=["John Doe"])


# ========== 创建 Schema ==========
class UserCreate(UserBase):
    """创建用户时的输入数据"""

    password: str = Field(
        ..., min_length=8, max_length=100, description="密码（至少8位）", examples=["SecurePass123"]
    )


# ========== 更新 Schema ==========
class UserUpdate(BaseModel):
    """更新用户时的输入数据（所有字段都是可选的）"""

    email: EmailStr | None = None
    username: str | None = Field(None, min_length=3, max_length=50)
    full_name: str | None = Field(None, max_length=100)
    password: str | None = Field(None, min_length=8, max_length=100)
    is_active: bool | None = None


# ========== 响应 Schema ==========
class UserResponse(UserBase):
    """返回给客户端的用户数据（不包含密码）"""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    # 序列化器：自定义 datetime 格式
    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, dt: datetime | None, _info) -> str | None:
        """
        将 datetime 序列化为指定格式：YYYY-MM-DD HH:MM:SS

        处理：
        1. None 值返回 None
        2. 自动转换为配置的时区
        3. 格式化为可读字符串
        """
        if dt is None:
            return None

        # 如果是 naive datetime（无时区信息），假设为 UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))

        # 转换为目标时区
        local_dt = dt.astimezone(ZoneInfo(settings.TIMEZONE))

        return local_dt.strftime("%Y-%m-%d %H:%M:%S")

    # Pydantic V2 配置
    model_config = ConfigDict(
        from_attributes=True,  # 允许从 ORM 对象创建（以前的 orm_mode）
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2025-10-22 13:54:07",
                "updated_at": "2025-10-22 13:54:07",
            }
        },
    )


# ========== 数据库内部使用 Schema ==========
class UserInDB(UserBase):
    """数据库中的用户数据（包含敏感信息，仅内部使用）"""

    id: int
    hashed_password: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ========== 列表响应 Schema ==========
class UserListResponse(BaseModel):
    """用户列表响应（带分页）"""

    total: int = Field(..., description="总数")
    items: list[UserResponse] = Field(..., description="用户列表")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 100,
                "items": [
                    {
                        "id": 1,
                        "email": "user1@example.com",
                        "username": "user1",
                        "full_name": "User One",
                        "is_active": True,
                        "is_superuser": False,
                        "created_at": "2025-10-22 13:54:07",
                        "updated_at": "2025-10-22 13:54:07",
                    }
                ],
                "page": 1,
                "page_size": 10,
            }
        }
    )


# Schema 设计最佳实践：
# 1. 分离不同用途的 Schema（Create, Update, Response）
# 2. 使用继承避免重复（UserBase）
# 3. Create Schema 所有字段必填
# 4. Update Schema 所有字段可选
# 5. Response Schema 不包含敏感信息（如密码）
# 6. 使用 Field 添加验证、描述和示例
# 7. 使用 json_schema_extra 提供完整示例
# 8. 使用 field_serializer 自定义序列化逻辑（处理 None 和时区）
