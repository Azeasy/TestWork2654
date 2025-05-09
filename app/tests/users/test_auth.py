import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(client, db_session):
    response = await client.post(
        "/auth/register",
        json={"name": "Name", "email": "test2@example.com", "password": "testpass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test2@example.com"
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_login_user(client):
    # First register a user
    await client.post(
        "/auth/register",
        json={"name": "Johan", "email": "test1@example.com", "password": "testpass123"}
    )

    # Then try to login
    response = await client.post(
        "/auth/login",
        json={"email": "test1@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_login_wrong_password(client):
    # First register a user
    await client.post(
        "/auth/register",
        json={"email": "test3@example.com", "password": "testpass123"}
    )

    # Try to login with wrong password
    response = await client.post(
        "/auth/login",
        json={"email": "test3@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
