import pytest, httpx, time
from realTest import deleteAll

address = "http://0.0.0.0:8001"
# address = "http://ube-schedule.com"

access_token = ""
refresh_token = ""

@pytest.mark.asyncio
async def testCorrectUserSignup(client=httpx.AsyncClient(base_url=address)) -> None:
    payload = {
        "email": "this_user_is_a_test_of_signup@accesscontrol.com",
        "password": "ThisIsATestOfSignupPassword",
    }
    headers = {"Content-Type": "application/json"}
    testResponse = {"status": "User created successfully"}
    testResponse2 = {"detail": "This email is already registered"}

    response = await client.post(url="/api/v1/internal/auth/signup", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

    response = await client.post(url="/api/v1/internal/auth/signup", json=payload, headers=headers)
    assert response.status_code == 409
    assert response.json() == testResponse2



@pytest.mark.asyncio
async def testCorrectUserSignin(client=httpx.AsyncClient(base_url=address)) -> None:
    correct = {
        "username": "this_user_is_a_test_of_signup@accesscontrol.com",
        "password": "ThisIsATestOfSignupPassword"
    }
    incorrectMail = {
        "username": "this_user_does_not_exist@accesscontrol.com",
        "password": "ThisIsATestOfSignupPassword"
    }
    incorrectPassword= {
        "username": "this_user_is_a_test_of_signup@accesscontrol.com",
        "password": "ThisIsNotARightPassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    testResponse = {"detail": "User with email does not exist"}
    testResponsePassword = {"detail": "Invalid details passed"}

    response = await client.post(url="/api/v1/internal/auth/signin", data=correct, headers=headers)
    assert response.status_code == 200
    response = response.json()
    assert "access_token" in response
    assert response["token_type"] == "Bearer"
    print(response)

    global access_token
    global refresh_token
    access_token = response["access_token"]
    refresh_token = response["refresh_token"]

    response = await client.post(url="/api/v1/internal/auth/signin", data=incorrectMail, headers=headers)
    assert response.status_code == 404
    assert response.json() == testResponse

    # for i in range(5):
    #     response = await client.post(url="/api/v1/internal/auth/signin", data=incorrectPassword, headers=headers)
    #     assert response.status_code == 401
    #     assert response.json() == testResponsePassword
    # response = await client.post(url="/api/v1/internal/auth/signin", data=incorrectPassword, headers=headers)
    # assert response.status_code == 429
    # print("What we are waiting for: ",  response.json())
    # time.sleep(31)

    response = await client.post(url="/api/v1/internal/auth/signin", data=correct, headers=headers)
    assert response.status_code == 200
    response = response.json()
    assert "access_token" in response
    assert response["token_type"] == "Bearer"

@pytest.mark.asyncio
async def testTokenRefresh(client=httpx.AsyncClient(base_url=address)) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {refresh_token}"
    }
    response = await client.get(url="/api/v1/internal/auth/refresh", headers=headers)
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testMultipleSession(client=httpx.AsyncClient(base_url=address)) -> None:
    tokens = []
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    for _ in range(4):
        payload = {
            "username": "this_user_is_a_test_of_signup@accesscontrol.com",
            "password": "ThisIsATestOfSignupPassword"
        }
        response = await client.post(url="/api/v1/internal/auth/signin", data=payload, headers=headers)
        assert response.status_code == 200
        tokens.append(response.json())

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tokens[0]["access_token"]}"
    }
    testResponse = {"status": "User logged out successfully"}
    response = await client.post(url="/api/v1/internal/auth/logout", headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = await client.get(url="/api/v1/internal/auth/session", headers=headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 5

    print("Header: ", headers)
    payload = {"session_id": response[-1]["session_id"]}
    response = await client.post(url="/api/v1/internal/auth/logout-session", headers=headers, json=payload)
    assert response.status_code == 200

    response = await client.get(url="/api/v1/internal/auth/session", headers=headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 4

    response = await client.post(url="/api/v1/internal/auth/logout-all", headers=headers)
    testResponse = {"status": "Session logged out successfully", "countOfRemovedSessions": 3}
    assert response.status_code == 200
    assert response.json() == testResponse

    response = await client.get(url="/api/v1/internal/auth/session", headers=headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 1

@pytest.mark.asyncio
async def testDeleteUser(client=httpx.AsyncClient(base_url=address)) -> None:
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    testResponse = {"status": "User deleted successfully"}
    response = await client.delete(url="/api/v1/internal/auth/user", headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def deleteAllFromDB() -> None:
    deleteAll()
