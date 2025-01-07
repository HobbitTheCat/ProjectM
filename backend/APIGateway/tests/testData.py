import pytest, httpx
token = ""

@pytest.mark.asyncio
async def testSignIn(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
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
    assert response.json()["token_type"] == "Bearer"

@pytest.mark.asyncio
async def testWeekSchedule(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/schedule/week?date=2025-01-06", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testDaySchedule(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/schedule/day?date=2025-01-06", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListGroups(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/group-list", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListGroupsFilter(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/group-list?sort=alphabet", headers=headers)
    assert response.status_code == 200
    print(response.json())


@pytest.mark.asyncio
async def testListTeacher(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/teacher-list", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListTeacherFilter(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/teacher-list?sort=alphabet", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListLocation(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/location-list", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListLocationFilter(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get(url="/api/v1/location-list?sort=alphabet", headers=headers)
    assert response.status_code == 200
    print(response.json())


@pytest.mark.asyncio
async def testPostHistory(client=httpx.AsyncClient(base_url="http://localhost:8000")) -> None:
    payload = {
        "items": [{"location": "AS07"}]
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    testResponse = {
        "status": "History added successfully"
    }
    response = await client.post(url="/api/v1/user/last-searched", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testPostFavorite(client=httpx.AsyncClient(base_url="http://localhost:8000")) -> None:
    payload = {
        "items": [{"location": "AS07"}]
    }
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    testResponse = {
        "status": "Favorite added successfully"
    }
    response = await client.post(url="/api/v1/user/favorite", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testGetFavorite(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/user/favorite", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetHistory(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = await client.get("/api/v1/user/last-searched", headers=headers)
    assert response.status_code == 200
    print(response.json())