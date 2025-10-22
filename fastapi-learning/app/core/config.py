"""
应用配置模块
使用 pydantic-settings 管理配置，支持从环境变量和 .env 文件读取
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基本信息
    APP_NAME: str = "FastAPI Learning"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"

    # 安全配置
    SECRET_KEY: str  # 必需，用于 JWT 签名
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS 配置
    BACKEND_CORS_ORIGINS: list[str] = []

    # 时区配置
    TIMEZONE: str = "Asia/Shanghai"  # 默认使用中国时区

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """将字符串形式的 CORS 源转换为列表"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    # Pydantic V2 配置
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # 忽略额外的环境变量
    )


# 创建全局配置实例
settings = Settings()


# 打印配置信息（仅用于学习和调试）
def print_settings() -> None:
    """打印当前配置（隐藏敏感信息）"""
    print("=" * 60)
    print("📋 应用配置信息")
    print("=" * 60)
    print(f"应用名称: {settings.APP_NAME}")
    print(f"版本: {settings.APP_VERSION}")
    print(f"调试模式: {settings.DEBUG}")
    print(f"数据库: {settings.DATABASE_URL}")
    print(f"密钥: {'*' * len(settings.SECRET_KEY)}")
    print(f"Token 过期时间: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} 分钟")
    print(f"允许的 CORS 源: {settings.BACKEND_CORS_ORIGINS}")
    print("=" * 60)


if __name__ == "__main__":
    # 测试配置加载
    print_settings()
