# 安装依赖: pip install pydantic-settings[yaml]

"""
Pydantic 元类冲突问题详解

问题：当尝试为 BaseSettings 添加单例元类时会遇到元类冲突
解决：需要继承 Pydantic 的 ModelMetaclass
"""

from typing import Tuple, Type
from pathlib import Path
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource
)


# ============================================================================
# 问题演示：元类冲突
# ============================================================================

print("=" * 70)
print("问题：元类冲突")
print("=" * 70)

print("""
当你尝试这样做时：

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        ...

class Settings(BaseSettings, metaclass=SingletonMeta):  # ❌ 错误！
    pass

会得到错误：
TypeError: metaclass conflict: the metaclass of a derived class 
must be a (non-strict) subclass of the metaclasses of all its bases

原因：BaseSettings 已经有自己的元类 (ModelMetaclass)
""")


# ============================================================================
# 解决方案 1: 继承正确的元类（推荐用于单例模式）
# ============================================================================

print("\n" + "=" * 70)
print("解决方案 1: 继承 ModelMetaclass")
print("=" * 70)

from pydantic._internal._model_construction import ModelMetaclass


class SingletonMeta(ModelMetaclass):
    """
    正确的单例元类实现
    继承 ModelMetaclass 避免元类冲突
    """
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            print(f"  🔨 创建新实例: {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            print(f"  ♻️  返回已存在的实例: {cls.__name__}")
        return cls._instances[cls]
    
    @classmethod
    def clear_instances(cls):
        """清除所有单例实例（用于测试）"""
        cls._instances.clear()


# 准备配置文件
PROJECT_ROOT = Path(__file__).parent
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "app.yaml"

CONFIG_DIR.mkdir(exist_ok=True)
yaml_content = """
app_name: "Singleton App"
debug: true
secret_key: "secret-123"
"""
with open(CONFIG_FILE, "w", encoding="utf-8") as f:
    f.write(yaml_content)


class SingletonSettings(BaseSettings, metaclass=SingletonMeta):
    """使用单例元类的配置类"""
    model_config = SettingsConfigDict(
        yaml_file=str(CONFIG_FILE),
        yaml_file_encoding="utf-8",
    )
    
    app_name: str
    debug: bool
    secret_key: str
    
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
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


print("\n测试单例模式:")
print("-" * 70)

print("\n1️⃣  第一次实例化:")
s1 = SingletonSettings()
print(f"   实例 ID: {id(s1)}")
print(f"   app_name: {s1.app_name}")

print("\n2️⃣  第二次实例化:")
s2 = SingletonSettings()
print(f"   实例 ID: {id(s2)}")
print(f"   是同一个实例: {s1 is s2}")

print("\n3️⃣  即使用不同参数也返回同一实例:")
s3 = SingletonSettings(app_name="Different Name")  # 参数被忽略
print(f"   实例 ID: {id(s3)}")
print(f"   app_name (未改变): {s3.app_name}")
print(f"   是同一个实例: {s1 is s3}")


# ============================================================================
# 解决方案 2: 使用 __new__ 方法（更简单，推荐）
# ============================================================================

print("\n" + "=" * 70)
print("解决方案 2: 使用 __new__ 方法（更简单）")
print("=" * 70)

print("""
不需要元类，直接重写 __new__ 方法：
""")


class SingletonSettings2(BaseSettings):
    """使用 __new__ 实现单例"""
    _instance = None
    
    model_config = SettingsConfigDict(
        yaml_file=str(CONFIG_FILE),
        yaml_file_encoding="utf-8",
    )
    
    app_name: str
    debug: bool
    secret_key: str
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("  🔨 创建新实例 (使用 __new__)")
            cls._instance = super().__new__(cls)
        else:
            print("  ♻️  返回已存在的实例 (使用 __new__)")
        return cls._instance
    
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
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


print("\n测试 __new__ 单例:")
print("-" * 70)

print("\n1️⃣  第一次实例化:")
ss1 = SingletonSettings2()
print(f"   实例 ID: {id(ss1)}")

print("\n2️⃣  第二次实例化:")
ss2 = SingletonSettings2()
print(f"   实例 ID: {id(ss2)}")
print(f"   是同一个实例: {ss1 is ss2}")


# ============================================================================
# 解决方案 3: 使用 @lru_cache（最推荐）
# ============================================================================

print("\n" + "=" * 70)
print("解决方案 3: 使用 @lru_cache（最简单最推荐）")
print("=" * 70)

from functools import lru_cache


class NormalSettings(BaseSettings):
    """普通的配置类"""
    model_config = SettingsConfigDict(
        yaml_file=str(CONFIG_FILE),
        yaml_file_encoding="utf-8",
    )
    
    app_name: str
    debug: bool
    secret_key: str
    
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
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


@lru_cache
def get_settings() -> NormalSettings:
    """使用 @lru_cache 实现单例"""
    print("  🔨 创建新实例 (使用 @lru_cache)")
    return NormalSettings()


print("\n测试 @lru_cache 单例:")
print("-" * 70)

print("\n1️⃣  第一次调用:")
gs1 = get_settings()
print(f"   实例 ID: {id(gs1)}")

print("\n2️⃣  第二次调用:")
gs2 = get_settings()
print(f"   实例 ID: {id(gs2)}")
print(f"   是同一个实例: {gs1 is gs2}")

print("\n3️⃣  可以清除缓存重新加载:")
get_settings.cache_clear()
gs3 = get_settings()
print(f"   新实例 ID: {id(gs3)}")
print(f"   与之前不同: {gs1 is not gs3}")


# ============================================================================
# 方案对比总结
# ============================================================================

print("\n" + "=" * 70)
print("📊 方案对比")
print("=" * 70)

comparison = """
┌─────────────────┬──────────────┬────────────┬──────────┬──────────┐
│ 方案            │ 代码复杂度   │ 测试友好度 │ 线程安全 │ 推荐度   │
├─────────────────┼──────────────┼────────────┼──────────┼──────────┤
│ 元类 (Solution1)│ ★★★★☆       │ ★★☆☆☆     │ ★★★★★   │ ★★☆☆☆   │
│ __new__         │ ★★★☆☆       │ ★★☆☆☆     │ ★★★★★   │ ★★★☆☆   │
│ @lru_cache      │ ★☆☆☆☆       │ ★★★★★     │ ★★★★★   │ ★★★★★   │
└─────────────────┴──────────────┴────────────┴──────────┴──────────┘

推荐使用：@lru_cache 方案
理由：
✅ 代码最简单
✅ 测试最友好（可以 .cache_clear()）
✅ 线程安全
✅ FastAPI 官方推荐
✅ 不需要处理元类冲突
"""

print(comparison)


# ============================================================================
# 最佳实践代码模板
# ============================================================================

print("\n" + "=" * 70)
print("💡 最佳实践代码模板")
print("=" * 70)

print("""
# config.py
from functools import lru_cache
from pathlib import Path
from typing import Tuple, Type
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PydanticBaseSettingsSource
)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        yaml_file="config.yaml",
        yaml_file_encoding="utf-8",
    )
    
    # 你的配置字段
    app_name: str
    debug: bool = False
    
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
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


# 使用方式
# ---------
# 在其他文件中：
from config import get_settings

settings = get_settings()
print(settings.app_name)

# FastAPI 中：
from fastapi import Depends

@app.get("/")
def read_root(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name}
""")

print("\n" + "=" * 70)
print("🎯 总结")
print("=" * 70)
print("""
遇到元类冲突问题时：

1. 如果必须用元类（比如实现复杂的单例逻辑）：
   ✅ 继承 ModelMetaclass 而不是 type

2. 如果只是想实现单例：
   ✅ 推荐使用 @lru_cache（最简单）
   ✅ 或者使用 __new__ 方法

3. 避免不必要的复杂度：
   ❌ 大多数情况下不需要元类
   ❌ 元类会让代码难以理解和维护
""")