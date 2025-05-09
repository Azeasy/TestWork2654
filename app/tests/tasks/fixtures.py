import pytest
import pytest_asyncio
from app.tasks.models import Task


@pytest_asyncio.fixture(scope="session")
async def test_task(test_user, db_session):
    task = Task(
        title="Test Task",
        description="Test Description",
        priority=0,
        owner_id=test_user.id
    )
    db_session.add(task)
    await db_session.commit()
    return task


@pytest_asyncio.fixture(scope="session")
async def test_tasks(test_user, db_session):
    tasks = [
        Task(
            title=f"Test Task {i}",
            description=f"Test Description {i}",
            priority=i,
            owner_id=test_user.id
        ) for i in range(3)
    ]
    db_session.add_all(tasks)
    await db_session.commit()
    return tasks
