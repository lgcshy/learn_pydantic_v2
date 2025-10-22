"""
FastAPI 主应用入口
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import init_db


# 生命周期事件处理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print("🚀 应用启动中...")
    print(f"📦 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🔧 调试模式: {settings.DEBUG}")

    # 初始化数据库表
    init_db()

    print("✅ 应用启动完成")
    print("📖 API 文档: http://localhost:8000/docs")

    yield

    # 关闭时执行（如需要可在此处添加清理代码）


# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FastAPI + SQLAlchemy + Pydantic 学习项目",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# 配置 CORS 中间件
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# 根路径
@app.get("/", tags=["根"])
def root():
    """根路径"""
    return {
        "message": "欢迎使用 FastAPI 学习项目！",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": settings.APP_VERSION,
    }


# 健康检查
@app.get("/health", tags=["健康检查"])
def health_check():
    """健康检查端点"""
    return {"status": "healthy", "app": settings.APP_NAME}


# 注册 API 路由
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    # 开发环境运行
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 自动重载
        log_level="info",
    )
