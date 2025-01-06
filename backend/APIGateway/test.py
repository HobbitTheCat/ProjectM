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
