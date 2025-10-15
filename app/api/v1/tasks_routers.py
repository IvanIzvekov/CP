from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.dependencies.auth_depend import check_auth_dep
from app.dependencies.premission_depend import check_upload_permission
from app.entities.task import TaskEntity
from app.entities.user import UserEntity
from app.exceptions.exceptions import ResponsibleTypeError, UserNotFoundError
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task_schema import TaskCreate, TaskDelete, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
async def task_create(
    data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    user: UserEntity = Depends(check_auth_dep),
):
    service = TaskService(TaskRepository(session), UserRepository(session))
    try:
        task = await service.create(
            responsible_id=user.id,
            text=data.text,
            owner_id=user.id,
            responsible_type="user",
            can_be_completed=data.can_be_completed,
            can_be_deleted=data.can_be_deleted,
        )
    except ResponsibleTypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    task_map = task.to_dict()
    return {"task": task_map, "detail": "Task created successfully"}


@router.post("/{responsible_type}/{responsible_id}")
async def user_task_create(
    data: TaskCreate,
    responsible_type: Literal["user", "duty"] = Path(
        ..., description="Тип ответственного: user или duty"
    ),
    responsible_id: UUID = Path(
        ...,
        description="ID ответственного (пользователь или группа по обязанности)",
    ),
    session: AsyncSession = Depends(get_session),
    user: UserEntity = Depends(check_auth_dep),
):
    pass


@router.get("/")
async def task_get(
    session: AsyncSession = Depends(get_session),
    user: UserEntity = Depends(check_auth_dep),
):
    pass


@router.get("/{user_id}")
async def task_get(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    user: UserEntity = Depends(check_auth_dep),
):
    pass


@router.delete("/")
async def task_get(
    data: TaskDelete,
    session: AsyncSession = Depends(get_session),
    user: UserEntity = Depends(check_auth_dep),
):
    pass


@router.patch("/")
async def task_get(
    data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    user: UserEntity = Depends(check_auth_dep),
):
    pass
