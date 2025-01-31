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
    print(token)
    assert response.json()["token_type"] == "Bearer"

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