import pytest
from app.core.config import settings


@pytest.mark.asyncio(loop_scope="session")
async def test_create_task(client, test_user_token: str):
    response = await client.post(
        "/tasks",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json={
            "title": "New Task",
            "description": "Task Description",
            "status": "pending",
            "priority": 0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Task Description"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_get_task(client, test_user_token: str, test_task):
    response = await client.get(
        f"/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_task.id
    assert data["title"] == test_task.title
    assert data["description"] == test_task.description


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks(client, test_user_token: str, test_tasks):
    response = await client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


@pytest.mark.asyncio(loop_scope="session")
async def test_search_tasks(client, test_user_token: str, test_tasks):
    response = await client.get(
        "/tasks/search?q=Test Task 1",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task 1"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_task_unauthorized(client):
    response = await client.post(
        "/tasks",
        json={
            "title": "New Task",
            "description": "Task Description"
        }
    )
    assert response.status_code == 403


@pytest.mark.asyncio(loop_scope="session")
async def test_get_nonexistent_task(client, test_user_token: str):
    response = await client.get(
        "/tasks/999999",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )
    assert response.status_code == 404
