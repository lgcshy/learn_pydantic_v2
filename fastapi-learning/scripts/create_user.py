"""
创建初始用户的脚本
用于测试和开发
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal, init_db  # noqa: E402
from app.crud.user import user_crud  # noqa: E402


def create_initial_users():
    """创建初始测试用户"""
    print("=" * 60)
    print("🔧 创建初始用户")
    print("=" * 60)

    # 初始化数据库
    init_db()

    db = SessionLocal()

    try:
        from app.schemas.user import UserCreate

        # 创建普通用户
        print("\n📝 创建普通用户...")
        existing_user = user_crud.get_by_username(db, username="testuser")
        if not existing_user:
            user_in = UserCreate(
                email="user@example.com",
                username="testuser",
                password="password123",
                full_name="Test User",
            )
            user = user_crud.create(db, obj_in=user_in)
            print(f"✅ 普通用户创建成功: {user.username} ({user.email})")
        else:
            print(f"⚠️  用户已存在: {existing_user.username}")

        # 创建管理员用户
        print("\n👑 创建管理员用户...")
        existing_admin = user_crud.get_by_username(db, username="admin")
        if not existing_admin:
            admin_in = UserCreate(
                email="admin@example.com",
                username="admin",
                password="admin123",
                full_name="Admin User",
            )
            admin = user_crud.create(db, obj_in=admin_in)
            # 设置为管理员
            admin.is_superuser = True
            db.commit()
            print(f"✅ 管理员创建成功: {admin.username} ({admin.email})")
        else:
            print(f"⚠️  管理员已存在: {existing_admin.username}")

        print("\n" + "=" * 60)
        print("📋 测试账号信息")
        print("=" * 60)
        print("\n普通用户:")
        print("  用户名: testuser")
        print("  密码: password123")
        print("\n管理员:")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n" + "=" * 60)
        print("💡 提示:")
        print("  1. 访问 http://localhost:8000/docs 测试 API")
        print("  2. 使用上述账号登录获取 token")
        print("  3. 在 Swagger UI 中点击 'Authorize' 按钮输入 token")
        print("=" * 60)

    except Exception as e:
        print(f"❌ 错误: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_users()
