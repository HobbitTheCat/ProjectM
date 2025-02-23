import httpx
import pytest

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1MjU2MDAsInVzZXJfaWQiOjEsInJlZnJlc2giOmZhbHNlLCJleHAiOjE3Mzk0NjUwMTZ9.MtNUdHz3JKpxfX7NV5fzvQaRMdHj68wZopyGsvv3_h8"
address = "http://0.0.0.0:8006"

headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

@pytest.mark.asyncio
async def testUserCreation(client=httpx.AsyncClient(base_url=address)):
    payload = {
        "username": "Egor_Semenov-Tyan-Shanskiy@etu.u-bourgogne.fr",
        "uid": "1",
    }
    response = await client.post("/api/v1/internal/user", json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def testUserRead(client=httpx.AsyncClient(base_url=address)):
    response = await client.get("/api/v1/internal/user", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testUserUpdateName(client=httpx.AsyncClient(base_url=address)):
    payload = {"name": "Denis"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/internal/user/name", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testUserUpdateBirthday(client=httpx.AsyncClient(base_url=address)):
    payload = {"birthday": "2011-07-07"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/internal/user/birthday", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

    payload = {"birthday": "notADate"}
    response = await client.put("/api/v1/internal/user/birthday", headers=headers, json=payload)
    assert response.status_code == 422

    payload = {"birthday": "2011-13-07"}
    response = await client.put("/api/v1/internal/user/birthday", headers=headers, json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def testUserUpdateGroup(client=httpx.AsyncClient(base_url=address)):
    payload = {"name": "IE4-I42"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/internal/user/group", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testUserUpdateTheme(client=httpx.AsyncClient(base_url=address)):
    payload = {"theme": "dark"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/internal/user/theme", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

    payload = {"theme": "notATheme"}
    response = await client.put("/api/v1/internal/user/theme", headers=headers, json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def testUserUpdateFavorite(client=httpx.AsyncClient(base_url=address)):
    payload = {"items": [{"name": "Mr. Smith", "type": "Teacher"},
                         {"name": "MI4-FC", "type":"Group"},
                         {"name": "IE4-I41", "type":"Group"}]}
    response = await client.post("/api/v1/internal/user/favorite", headers=headers, json=payload)
    assert response.status_code == 404
    print(response.json())
    payload = {"items": [{"name": "MI4-FC", "type": "Group"},
                         {"name": "IE4-I41", "type": "Group"}]}
    response = await client.post("/api/v1/internal/user/favorite", headers=headers, json=payload)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testUserDeleteFavorite(client=httpx.AsyncClient(base_url=address)):
    response = await client.delete("/api/v1/internal/user/favorite?index=1", headers=headers)
    assert response.status_code == 200
    print(response.json())

    response = await client.delete("/api/v1/internal/user/favorite?index=1", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def testAddHistory(client=httpx.AsyncClient(base_url=address)):
    payload={
        "name": "MI4-06",
        "type": "Group"
    }
    response = await client.post("/api/v1/internal/user/history", json=payload, headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testUserRead(client=httpx.AsyncClient(base_url=address)):
    response = await client.get("/api/v1/internal/user", headers=headers)
    assert response.status_code == 200
    print(response.json())
