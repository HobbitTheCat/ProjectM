import pytest
import httpx


@pytest.mark.asyncio
async def testSignup(client = httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    payload = {
        "email": "this_user_is_a_test_of_signup@apigateway.com",
        "password": "ThisIsATestOfSignupPassword"
    }
    headers = {"Content-Type": "application/json"}
    testResponse = {"status": "User created successfully"}

    response = await client.post(url="/api/v1/user/auth/signup", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testIncorrectUserSignup(client = httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    payload = {
        "email": "this_user_is_a_test_of_signup@apigateway.com",
        "password": "ThisIsATestOfSignupPassword",
    }
    headers = {"Content-Type": "application/json"}
    testResponse = {"detail": "This email is already registered"}

    response = await client.post(url="/api/v1/user/auth/signup", json=payload, headers=headers)
    assert response.status_code == 409
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testCorrectSignIn(client = httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    payload = {
        "username": "this_user_is_a_test_of_signup@apigateway.com",
        "password": "ThisIsATestOfSignupPassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await client.post(url="/api/v1/user/auth/signin", data=payload, headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "Bearer"

@pytest.mark.asyncio
async def testIncorrectUserSignin(client = httpx.AsyncClient(base_url="http://localhost:8000")) -> None:
    payload = {
        "username": "this_user_does_not_exist@apigateway.com",
        "password": "ThisIsATestOfSignupPassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    testResponse = {
        "detail": "User with email does not exist",
    }

    response = await client.post(url="/api/v1/user/auth/signin", data=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testIncorrectPasswordSignin(client=httpx.AsyncClient(base_url="http://0.0.0.0:8000")) -> None:
    payload = {
        "username": "this_user_is_a_test_of_signup@apigateway.com",
        "password": "NotTightPassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    testResponse = {
        "detail": "Invalid details passed",
    }
    response = await client.post(url="/api/v1/user/auth/signin", data=payload, headers=headers)
    assert response.status_code == 401
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testRemoveUserSuccess(client = httpx.AsyncClient(base_url="http://localhost:8000")) -> None:
    payload = {
        "username": "this_user_is_a_test_of_signup@apigateway.com",
        "password": "ThisIsATestOfSignupPassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    testResponse = {
        "status": "User successfully removed",
    }
    response = await client.post(url="/api/v1/user/auth/remove", data=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testRemoveUserFailure(client = httpx.AsyncClient(base_url="http://localhost:8000")) -> None:
    payload = {
        "username": "this_user_is_a_test_of_signup@accesscontrol.com",
        "password": "ThisIsATestOfSignupPassword"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    testResponse = {
        "detail": "User with email does not exist",
    }
    response = await client.post(url="/api/v1/user/auth/remove", data=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == testResponse