# 安装依赖: pip install pydantic-settings[yaml]

import os
import time
from functools import lru_cache
from pathlib import Path
from typing import Tuple, Type

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource, PydanticBaseSettingsSource


# ============================================================================
# 准备工作：创建配置文件
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
CONFIG_DIR = PROJECT_ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "app.yaml"


def setup_config():
    """创建示例配置文件"""
    CONFIG_DIR.mkdir(exist_ok=True)
    yaml_content = """
app_name: "MyApp"
debug: false
secret_key: "super-secret-key"
database:
  host: "localhost"
  port: 5432
  username: "user"
  password: "pass"
"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(yaml_content)


class DatabaseSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    username: str
    password: str


class AppSettings(BaseSettings):
    """
    关键点：Pydantic Settings v2 需要显式配置 settings_customise_sources
    """
    model_config = SettingsConfigDict(
        yaml_file=str(CONFIG_FILE),
        yaml_file_encoding="utf-8",
        extra="ignore"
    )
    
    app_name: str
    debug: bool
    secret_key: str
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    
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
        自定义配置源的优先级
        
        优先级从高到低：
        1. init_settings - 初始化时传入的参数
        2. env_settings - 环境变量
        3. YamlConfigSettingsSource - YAML 配置文件
        4. file_secret_settings - 文件密钥
        """
        return (
            init_settings,
            env_settings,
            YamlConfigSettingsSource(settings_cls),
            file_secret_settings,
        )
    
    def __init__(self, **kwargs):
        print(f"⚙️  AppSettings 初始化被调用！时间: {time.time()}")
        super().__init__(**kwargs)


# ============================================================================
# 方式 1: 使用 @lru_cache 装饰器（FastAPI 推荐）
# ============================================================================

@lru_cache
def get_settings_with_cache() -> AppSettings:
    """
    使用 @lru_cache 确保只创建一次
    
    优点：
    1. 懒加载 - 只在第一次调用时才初始化
    2. 线程安全
    3. 可以有参数（虽然这里没用到）
    4. 便于测试 - 可以用 .cache_clear() 清除缓存
    """
    return AppSettings()


# ============================================================================
# 方式 2: 模块级直接实例化（看起来更优雅）
# ============================================================================

# 先创建配置文件，再实例化
setup_config()

# ⚠️ 注意：这行代码在模块导入时就会执行！
settings_direct = AppSettings()


# ============================================================================
# 方式 3: 单例元类（传统方式）- 需要处理元类冲突
# ============================================================================

# 获取 BaseSettings 的元类
from pydantic._internal._model_construction import ModelMetaclass

class SingletonMeta(ModelMetaclass):
    """
    继承自 Pydantic 的 ModelMetaclass 避免元类冲突
    """
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonSettings(AppSettings, metaclass=SingletonMeta):
    """使用单例元类"""
    pass


def get_settings_singleton() -> SingletonSettings:
    return SingletonSettings()


# ============================================================================
# 对比测试
# ============================================================================

def test_lru_cache():
    """测试 @lru_cache 方式"""
    print("\n" + "=" * 70)
    print("测试方式 1: @lru_cache 装饰器")
    print("=" * 70)
    
    print("\n1️⃣  第一次调用 get_settings_with_cache():")
    s1 = get_settings_with_cache()
    print(f"   实例 ID: {id(s1)}")
    print(f"   app_name: {s1.app_name}")
    
    print("\n2️⃣  第二次调用 get_settings_with_cache():")
    s2 = get_settings_with_cache()
    print(f"   实例 ID: {id(s2)}")
    
    print(f"\n✅ 是否为同一实例: {s1 is s2}")
    
    # 重点：可以清除缓存（便于测试）
    print("\n🧹 清除缓存: get_settings_with_cache.cache_clear()")
    get_settings_with_cache.cache_clear()
    
    print("\n3️⃣  清除缓存后再次调用:")
    s3 = get_settings_with_cache()
    print(f"   实例 ID: {id(s3)}")
    print(f"   与之前的实例相同吗: {s1 is s3}")


def test_direct_instance():
    """测试直接实例化方式"""
    print("\n" + "=" * 70)
    print("测试方式 2: 模块级直接实例化")
    print("=" * 70)
    
    print("\n⚠️  注意：settings_direct 在模块导入时就已经初始化了！")
    print(f"   实例 ID: {id(settings_direct)}")
    print(f"   app_name: {settings_direct.app_name}")
    
    print("\n1️⃣  访问 settings_direct:")
    print(f"   实例 ID: {id(settings_direct)}")
    
    print("\n2️⃣  再次访问 settings_direct:")
    print(f"   实例 ID: {id(settings_direct)}")
    
    print(f"\n✅ 永远是同一个实例")


def test_singleton_meta():
    """测试单例元类方式"""
    print("\n" + "=" * 70)
    print("测试方式 3: 单例元类")
    print("=" * 70)
    
    print("\n1️⃣  第一次调用 get_settings_singleton():")
    s1 = get_settings_singleton()
    print(f"   实例 ID: {id(s1)}")
    print(f"   app_name: {s1.app_name}")
    
    print("\n2️⃣  第二次调用 get_settings_singleton():")
    s2 = get_settings_singleton()
    print(f"   实例 ID: {id(s2)}")
    
    print(f"\n✅ 是否为同一实例: {s1 is s2}")


def test_import_timing():
    """测试导入时机的影响"""
    print("\n" + "=" * 70)
    print("🔍 关键区别：导入时机")
    print("=" * 70)
    
    print("\n方式 1 (@lru_cache):")
    print("  - ✅ 懒加载：只在第一次调用 get_settings_with_cache() 时初始化")
    print("  - ✅ 如果这个模块被导入但函数未被调用，不会初始化")
    
    print("\n方式 2 (直接实例化):")
    print("  - ⚠️  立即加载：import 这个模块时就会初始化")
    print("  - ⚠️  即使你只是导入其他东西，配置也会被加载")
    
    print("\n方式 3 (单例元类):")
    print("  - ✅ 懒加载：第一次调用时才初始化")
    print("  - ❌ 比较复杂，代码可读性差")


def test_testing_friendliness():
    """测试友好性对比"""
    print("\n" + "=" * 70)
    print("🧪 测试友好性对比")
    print("=" * 70)
    
    print("\n方式 1 (@lru_cache):")
    print("  - ✅ 可以用 .cache_clear() 清除缓存")
    print("  - ✅ 测试时可以轻松重新加载配置")
    print("  - ✅ 可以在测试中 mock 这个函数")
    
    print("\n方式 2 (直接实例化):")
    print("  - ❌ 模块级变量，测试时难以替换")
    print("  - ❌ 需要 reload 整个模块才能重新加载")
    print("  - ⚠️  测试隔离性差")
    
    print("\n方式 3 (单例元类):")
    print("  - ⚠️  需要手动清理 _instances 字典")
    print("  - ⚠️  测试时稍微麻烦一些")


def show_pydantic_v2_note():
    """说明 Pydantic v2 的重要变化"""
    print("\n" + "=" * 70)
    print("⚠️  Pydantic Settings v2 重要变化")
    print("=" * 70)
    
    print("""
在 Pydantic Settings v2 中，必须显式配置 YAML 配置源！

错误的做法（会报警告）：
    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            yaml_file="config.yaml"
        )

正确的做法：
    class Settings(BaseSettings):
        model_config = SettingsConfigDict(
            yaml_file="config.yaml"
        )
        
        @classmethod
        def settings_customise_sources(cls, ...):
            return (
                init_settings,
                env_settings,
                YamlConfigSettingsSource(settings_cls),  # 👈 关键
                file_secret_settings,
            )

这样做的好处：
1. 可以自定义配置源的优先级
2. 可以添加自定义配置源
3. 更加灵活和清晰
""")


def show_real_world_example():
    """真实场景示例"""
    print("\n" + "=" * 70)
    print("💡 真实场景示例")
    print("=" * 70)
    
    print("\n场景 1: FastAPI 应用")
    print("-" * 70)
    print("""
# 使用 @lru_cache（FastAPI 官方推荐）
from functools import lru_cache
from fastapi import Depends

@lru_cache
def get_settings():
    return Settings()

@app.get("/info")
def read_info(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name}

# 好处：
# 1. 依赖注入清晰
# 2. 测试时可以轻松 override
# 3. 懒加载，只在需要时初始化
""")
    
    print("\n场景 2: 简单脚本/小项目")
    print("-" * 70)
    print("""
# 直接实例化（更简洁）
from config import settings

def main():
    print(settings.app_name)
    
# 好处：
# 1. 代码简洁，直接使用
# 2. 不需要每次都调用函数
# 3. 适合小型项目，不需要复杂的测试
""")


def show_recommendation():
    """给出建议"""
    print("\n" + "=" * 70)
    print("📋 最佳实践建议")
    print("=" * 70)
    
    recommendations = {
        "✅ 使用 @lru_cache": [
            "FastAPI 或其他 Web 框架项目",
            "需要依赖注入的场景",
            "需要编写单元测试",
            "配置可能需要重新加载",
            "团队协作的大型项目"
        ],
        "✅ 使用直接实例化": [
            "简单的命令行工具",
            "一次性脚本",
            "小型项目（< 1000 行代码）",
            "不需要复杂测试",
            "配置简单且固定"
        ],
        "❌ 避免单例元类": [
            "除非有特殊需求",
            "增加代码复杂度",
            "大多数情况下 @lru_cache 更好"
        ]
    }
    
    for category, items in recommendations.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")


def main():
    """主测试函数"""
    print("\n🚀 配置单例模式对比演示")
    print("=" * 70)
    
    # 运行各种测试
    test_lru_cache()
    test_direct_instance()
    test_singleton_meta()
    test_import_timing()
    test_testing_friendliness()
    show_pydantic_v2_note()
    show_real_world_example()
    show_recommendation()
    
    print("\n" + "=" * 70)
    print("🎯 结论")
    print("=" * 70)
    print("""
你说得对，直接用 settings_direct 确实更优雅！

但 @lru_cache 的优势在于：
1. 懒加载 - 不用就不初始化（性能更好）
2. 测试友好 - 可以清除缓存重新加载
3. FastAPI 生态的标准做法

如果是小项目或简单脚本，直接实例化完全没问题，反而更简洁！
选择哪种方式取决于项目规模和需求。

⚠️  别忘了在 Pydantic Settings v2 中配置 settings_customise_sources！
""")


if __name__ == "__main__":
    main()