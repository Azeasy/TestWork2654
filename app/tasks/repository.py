from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from datetime import datetime
from app.tasks.models import Task
from app.tasks.schemas import TaskCreate, TaskUpdate
from typing import List


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task: TaskCreate, owner_id: int) -> Task:
        db_task = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            owner_id=owner_id
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update(self, task_id: int, task: TaskUpdate, owner_id: int) -> Task:
        query = select(Task).where(
            and_(Task.id == task_id, Task.owner_id == owner_id)
        )
        result = await self.db.execute(query)
        db_task = result.scalar_one_or_none()

        if db_task:
            for key, value in task.dict(exclude_unset=True).items():
                setattr(db_task, key, value)
            await self.db.commit()
            await self.db.refresh(db_task)
        return db_task

    async def get(self, task_id: int, owner_id: int) -> Task:
        query = select(Task).where(Task.owner_id == owner_id).where(Task.id == task_id)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list(
        self,
        owner_id: int,
        status=None,
        priority=None,
        created_from=None,
        created_to=None
    ) -> List[Task]:
        query = select(Task).where(Task.owner_id == owner_id)

        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if created_from:
            query = query.where(Task.created_at >= created_from)
        if created_to:
            query = query.where(Task.created_at <= created_to)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def search(self, owner_id: int, q: str) -> List[Task]:
        query = select(Task).where(
            Task.owner_id == owner_id,
            or_(
                Task.title.ilike(f"%{q}%"),
                Task.description.ilike(f"%{q}%")
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()
