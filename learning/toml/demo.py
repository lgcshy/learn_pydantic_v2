# 安装依赖: pip install pydantic-settings[toml]

from typing import Tuple, Type
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    TomlConfigSettingsSource,
    PydanticBaseSettingsSource,
)

PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "toml" / "config.toml"


class ServerSettings(BaseSettings):
    """服务器配置"""

    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    timeout: int = 30


class LoggingSettings(BaseSettings):
    """日志配置"""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "app.log"

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in allowed:
            raise ValueError(f"日志级别必须是: {', '.join(allowed)}")
        return v


class AppConfig(BaseSettings):
    """应用主配置"""

    model_config = SettingsConfigDict(
        toml_file=CONFIG_FILE,  # TOML 配置文件路径
        toml_file_encoding="utf-8",
        extra="ignore",
    )

    # 基本配置
    title: str = "My Application"
    version: str = "1.0.0"
    description: str = ""

    # 功能开关
    enable_cors: bool = True
    enable_docs: bool = True

    # 嵌套配置
    server: ServerSettings = Field(default_factory=ServerSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    # API 配置
    api_keys: list[str] = []
    rate_limit: int = 100

    # 环境配置
    environment: str = "development"

    # 设置自定义的设置源
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            TomlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


def main():
    # 创建示例 TOML 配置文件
    toml_content = """
# 应用基本信息
title = "My Awesome API"
version = "2.0.0"
description = "A powerful RESTful API"
environment = "production"

# 功能开关
enable_cors = true
enable_docs = false

# API 配置
api_keys = [
    "key-1234567890",
    "key-0987654321",
    "key-abcdefghij"
]
rate_limit = 200

# 服务器配置
[server]
host = "0.0.0.0"
port = 9000
workers = 8
timeout = 60

# 日志配置
[logging]
level = "WARNING"
format = "[%(levelname)s] %(asctime)s - %(message)s"
file = "production.log"
"""

    # 写入配置文件
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(toml_content)

    # 加载配置
    config = AppConfig()

    # 打印配置信息
    print("=" * 60)
    print("应用配置")
    print("=" * 60)
    print(f"标题: {config.title}")
    print(f"版本: {config.version}")
    print(f"描述: {config.description}")
    print(f"环境: {config.environment}")
    print()

    print("功能开关:")
    print("-" * 60)
    print(f"CORS: {'启用' if config.enable_cors else '禁用'}")
    print(f"API文档: {'启用' if config.enable_docs else '禁用'}")
    print()

    print("服务器配置:")
    print("-" * 60)
    print(f"监听地址: {config.server.host}:{config.server.port}")
    print(f"工作进程数: {config.server.workers}")
    print(f"超时时间: {config.server.timeout}秒")
    print()

    print("日志配置:")
    print("-" * 60)
    print(f"日志级别: {config.logging.level}")
    print(f"日志文件: {config.logging.file}")
    print(f"日志格式: {config.logging.format}")
    print()

    print("API 配置:")
    print("-" * 60)
    print(f"速率限制: {config.rate_limit} 请求/分钟")
    print(f"API 密钥数量: {len(config.api_keys)}")
    print("API 密钥列表:")
    for idx, key in enumerate(config.api_keys, 1):
        print(f"  {idx}. {key}")
    print()

    # 转换为字典
    print("完整配置 (JSON 格式):")
    print("-" * 60)
    import json

    print(json.dumps(config.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
