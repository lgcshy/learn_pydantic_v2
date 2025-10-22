"""
API v1 路由聚合
将所有端点路由组合到一起
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, users

# 创建 API v1 路由器
api_router = APIRouter()

# 注册各个模块的路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])

# 可以继续添加其他路由
# api_router.include_router(posts.router, prefix="/posts", tags=["文章"])
# api_router.include_router(comments.router, prefix="/comments", tags=["评论"])

