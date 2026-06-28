import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/users", json={
        "name": "New User",
        "email": "newuser@test.com",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New User"
    assert data["email"] == "newuser@test.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    await client.post("/api/users", json={"name": "First", "email": "dupe@test.com"})
    response = await client.post("/api/users", json={"name": "Second", "email": "dupe@test.com"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_users(client):
    response = await client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)