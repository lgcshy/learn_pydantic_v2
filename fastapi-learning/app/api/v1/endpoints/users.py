"""
用户管理相关的 API 端点
CRUD 操作
"""
from fastapi import APIRouter, HTTPException, Query, status

from app.api.v1.deps import CurrentSuperUser, CurrentUser, DBSession
from app.crud.user import user_crud
from app.schemas.user import UserListResponse, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", response_model=UserListResponse)
def get_users(
    db: DBSession,
    current_user: CurrentSuperUser,  # 需要管理员权限
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
) -> UserListResponse:
    """
    获取用户列表（分页）
    需要管理员权限
    """
    # 计算分页参数
    skip = (page - 1) * page_size

    # 获取用户列表
    users = user_crud.get_multi(db, skip=skip, limit=page_size)
    total = user_crud.get_count(db)

    return UserListResponse(
        total=total,
        items=users,
        page=page,
        page_size=page_size,
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> UserResponse:
    """
    根据 ID 获取用户
    需要认证
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    # 非管理员只能查看自己的信息
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> UserResponse:
    """
    更新用户信息
    需要认证（只能更新自己的信息或管理员可更新任何用户）
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    # 非管理员只能更新自己的信息
    if user.id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足",
        )

    # 如果更新邮箱，检查是否已存在
    if user_in.email and user_in.email != user.email:
        existing_user = user_crud.get_by_email(db, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被使用",
            )

    # 如果更新用户名，检查是否已存在
    if user_in.username and user_in.username != user.username:
        existing_user = user_crud.get_by_username(db, username=user_in.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该用户名已被使用",
            )

    # 非管理员不能修改 is_active 字段
    if not current_user.is_superuser and user_in.is_active is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法修改账号状态",
        )

    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: DBSession,
    current_user: CurrentSuperUser,  # 需要管理员权限
) -> None:
    """
    删除用户
    需要管理员权限
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    # 不能删除自己
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己",
        )

    user_crud.delete(db, id=user_id)

