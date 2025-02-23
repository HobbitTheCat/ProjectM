import pytest
import httpx

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1MjU2MDAsInVzZXJfaWQiOjEsInJlZnJlc2giOmZhbHNlLCJleHAiOjE3Mzk0NjUwMTZ9.MtNUdHz3JKpxfX7NV5fzvQaRMdHj68wZopyGsvv3_h8"
address = "http://0.0.0.0:8006"

headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }

@pytest.mark.asyncio
async def testCreateUser(client=httpx.AsyncClient(base_url=address)):
    payload={
        "uid": 1,
        "username": "egor_semenov-tyan-shanskiy@etu.u-bourgogne.fr"
    }
    response = await client.post("/api/v1/internal/user", json=payload)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetUser(client=httpx.AsyncClient(base_url=address)):
    response = await client.get(f"/api/v1/internal/user-info", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testDeleteUser(client=httpx.AsyncClient(base_url=address)):
    test_response = {"status": "user deleted successfully"}
    response = await client.delete(f"/api/v1/internal/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response

@pytest.mark.asyncio
async def testGetUser(client=httpx.AsyncClient(base_url=address)):
    response = await client.get(f"/api/v1/internal/user-info", headers=headers)
    assert response.status_code == 404
    print(response.json())