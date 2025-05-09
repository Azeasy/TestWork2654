from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.tasks.schemas import TaskCreate, TaskUpdate, TaskPartialUpdate, TaskRead
from app.tasks.service import TaskService
from app.tasks.enums import StatusEnum
from app.core.security import get_current_user
from app.db.session import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await TaskService(db).create_task(task, current_user.id)


@router.get("/search", response_model=List[TaskRead])
async def search_tasks(
    q: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await TaskService(db).search_tasks(current_user.id, q)


@router.get("/{task_id}", response_model=TaskRead)
async def retrieve_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return await TaskService(db).retrieve_task(task_id, current_user.id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return await TaskService(db).update_task(task_id, task, current_user.id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.patch("/{task_id}", response_model=TaskRead)
async def partial_update_task(
    task_id: int,
    task: TaskPartialUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return await TaskService(db).update_task(task_id, task, current_user.id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.get("", response_model=List[TaskRead])
async def list_tasks(
    status: StatusEnum = None,
    priority: int = None,
    created_from: datetime = Query(None),
    created_to: datetime = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await TaskService(db).list_tasks(current_user.id, status, priority, created_from, created_to)
