import httpx, pytest

address = "http://0.0.0.0:8000"
# address = "http://ube-schedule.com"

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
async def testUserRead(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = await client.get("/api/v1/user", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testUserUpdateName(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {"name": "Denis"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/user/name", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testUserUpdateBirthday(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {"birthday": "2011-07-07"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/user/birthday", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

    # payload = {"birthday": "notADate"}
    # response = await client.put("/api/v1/user/birthday", headers=headers, json=payload)
    # assert response.status_code == 422
    #
    # payload = {"birthday": "2011-13-07"}
    # response = await client.put("/api/v1/user/birthday", headers=headers, json=payload)
    # assert response.status_code == 422

@pytest.mark.asyncio
async def testUserUpdateGroup(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {"name": "IE4-I42"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/user/group", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testUserUpdateTheme(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {"theme": "dark"}
    testResponse = {"status": "success"}
    response = await client.put("/api/v1/user/theme", headers=headers, json=payload)
    assert response.status_code == 200
    assert response.json() == testResponse

    payload = {"theme": "notATheme"}
    response = await client.put("/api/v1/user/theme", headers=headers, json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def testUserUpdateFavorite(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = {"items": [{"name": "Mr. Smith", "type": "Teacher"},
                         {"name": "MI4-FC", "type":"Group"},
                         {"name": "IE4-I41", "type":"Group"}]}
    response = await client.post("/api/v1/user/favorite", headers=headers, json=payload)
    assert response.status_code == 404
    print(response.json())
    payload = {"items": [{"name": "MI4-FC", "type": "Group"},
                         {"name": "IE4-I41", "type": "Group"}]}
    response = await client.post("/api/v1/user/favorite", headers=headers, json=payload)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testUserDeleteFavorite(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = await client.delete("/api/v1/user/favorite?index=1", headers=headers)
    assert response.status_code == 200
    print(response.json())

    response = await client.delete("/api/v1/user/favorite?index=1", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def testAddHistory(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload={
        "name": "MI4-06",
        "type": "Group"
    }
    response = await client.post("/api/v1/user/history", json=payload, headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testUserRead2(client=httpx.AsyncClient(base_url=address)):
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = await client.get("/api/v1/user", headers=headers)
    assert response.status_code == 200
    print(response.json())
