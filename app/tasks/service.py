from app.tasks.repository import TaskRepository
from app.tasks.schemas import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db):
        self.repo = TaskRepository(db)

    async def retrieve_task(self, task_id: int, owner_id: int):
        result = await self.repo.get(task_id, owner_id)
        if not result:
            raise ValueError("Task not found")
        return result

    async def create_task(self, task: TaskCreate, owner_id: int):
        return await self.repo.create(task, owner_id)

    async def update_task(self, task_id: int, task: TaskUpdate, owner_id: int):
        updated = await self.repo.update(task_id, task, owner_id)
        if not updated:
            raise ValueError("Task not found")
        return updated

    async def list_tasks(self, owner_id: int, status=None, priority=None, created_from=None, created_to=None):
        return await self.repo.list(owner_id, status, priority, created_from, created_to)

    async def search_tasks(self, owner_id: int, q: str):
        return await self.repo.search(owner_id, q)
