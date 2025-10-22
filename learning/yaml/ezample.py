# 安装依赖: pip install pydantic-settings[yaml]

from typing import Tuple, Type
from pydantic import Field
from pydantic_settings import (
    BaseSettings, 
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource
)


class DatabaseSettings(BaseSettings):
    """数据库配置"""
    host: str = "localhost"
    port: int = 5432
    username: str
    password: str
    database: str = "mydb"


class AppSettings(BaseSettings):
    """应用配置"""
    model_config = SettingsConfigDict(
        yaml_file="config.yaml",  # YAML 配置文件路径
        yaml_file_encoding="utf-8",
        extra="ignore"  # 忽略配置文件中的额外字段
    )
    
    app_name: str = "MyApp"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    secret_key: str
    
    # 嵌套配置
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
    # 列表配置
    allowed_hosts: list[str] = ["localhost"]
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """
        配置源优先级（从高到低）：
        1. 初始化参数
        2. 环境变量
        3. YAML 配置文件
        4. 文件密钥
        """
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


def main():
    # 首先创建一个示例 YAML 配置文件
    yaml_content = """
app_name: "My Awesome App"
debug: true
host: "127.0.0.1"
port: 8080
secret_key: "super-secret-key-12345"

database:
  host: "db.example.com"
  port: 5432
  username: "admin"
  password: "admin123"
  database: "production_db"

allowed_hosts:
  - "localhost"
  - "example.com"
  - "*.example.com"
"""
    
    # 写入配置文件
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_content)
    
    # 加载配置
    settings = AppSettings()
    
    # 打印配置信息
    print("=" * 50)
    print("应用配置:")
    print("=" * 50)
    print(f"应用名称: {settings.app_name}")
    print(f"调试模式: {settings.debug}")
    print(f"监听地址: {settings.host}:{settings.port}")
    print(f"密钥: {settings.secret_key}")
    print()
    
    print("数据库配置:")
    print("-" * 50)
    print(f"主机: {settings.database.host}")
    print(f"端口: {settings.database.port}")
    print(f"用户名: {settings.database.username}")
    print(f"数据库: {settings.database.database}")
    print()
    
    print("允许的主机:")
    print("-" * 50)
    for host in settings.allowed_hosts:
        print(f"  - {host}")
    print()
    
    # 也可以转换为字典
    print("完整配置 (字典格式):")
    print("-" * 50)
    print(settings.model_dump())
    
    print("\n" + "=" * 50)
    print("💡 提示：环境变量可以覆盖配置文件")
    print("=" * 50)
    print("例如：")
    print("  export DATABASE__HOST=new-host.com")
    print("  export DEBUG=false")


if __name__ == "__main__":
    main()