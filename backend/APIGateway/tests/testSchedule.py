import pytest
import httpx

address = "http://0.0.0.0:8000"
# address = "https://ube-schedule.com"

token = ""

@pytest.mark.asyncio
async def testSignIn(client=httpx.AsyncClient(base_url=address)) -> None:
    payload ={
        "username": "permanent_test_user@mock.com",
        "password": "testPassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await client.post(url="/api/v1/user/auth/signin", data=payload, headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
    global token
    token = response.json()["access_token"]
    print(token)
    assert response.json()["token_type"] == "Bearer"

@pytest.mark.asyncio
async def testGetWeekSchedule(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/schedule/week?date=2025-01-27&group=MI4-FC", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetDaySchedule(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/schedule/day?date=2025-01-28&group=IE4-I42", headers=headers)
    assert response.status_code == 200
    response = await client.get("/api/v1/schedule/day?date=2025-01-44&group=IE4-I42", headers=headers)
    assert response.status_code == 422
    print(response.json())
    response = await client.get("/api/v1/schedule/day?date=2025-01-28&group=MI4-FC", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetGroupList(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/group-list", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetTeacherList(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/teacher-list", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetLocationList(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/location-list", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetGroupList(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/group-list?sort=asc", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)
    names = [item["name"] for item in data]
    assert names == sorted(names)

    response = await client.get("/api/v1/group-list?sort=desc", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(data)
    names = [item["name"] for item in data]
    assert names == sorted(names, reverse=True)

@pytest.mark.asyncio
async def testSearchItem(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/item-list?start=IS", headers=headers)
    assert response.status_code == 200
    print(response.json())

    response = await client.get("/api/v1/item-list?start=IS&sort=asc", headers=headers)
    assert response.status_code == 200
    print(response.json())