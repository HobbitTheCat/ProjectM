import pytest
import httpx
from dataBase.dataBaseConection import DataBase

@pytest.mark.asyncio
async def testMailCheckNotExist(client = httpx.AsyncClient(base_url="http://0.0.0.0:8002")) -> None:
    payload = {
        "email": "not_exist@mail.com",
    }
    headers = {
        "Content-Type": "application/json",
    }
    testResponse = {
        "status": False,
        "hash": None
    }
    response = await client.post(url="/api/v1/internal/data/check-mail", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testMailCheckExist(client = httpx.AsyncClient(base_url="http://0.0.0.0:8002")) -> None:
    payload = {
        "email": "test_user@mail.com",
    }
    headers = {
        "Content-Type": "application/json",
    }
    testResponse = {
        "status": True,
        "hash": "<hash>"
    }
    response = await client.post(url="/api/v1/internal/data/check-mail", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testUserAddExist(client = httpx.AsyncClient(base_url="http://0.0.0.0:8002")) -> None:
    username = "test_user@mail.com"
    payload = {
        "email": username,
        "password": "<hash>",
    }
    headers = {
        "Content-Type": "application/json",
    }
    testResponse = {
        "status":"User already exist"
    }
    response = await client.post(url="/api/v1/internal/data/create-user", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testUserAddNotExist(client = httpx.AsyncClient(base_url="http://0.0.0.0:8002")) -> None:
    username = "test_user_add@mail.com"
    payload = {
        "email": username,
        "password": "<hash>",
    }
    headers = {
        "Content-Type": "application/json",
    }
    testResponse = {
        "status":"User created successfully"
    }
    response = await client.post(url="/api/v1/internal/data/create-user", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse
    with DataBase() as db:
        existence = db.existUser(username)
    assert existence == True, "created but user does not exist"

@pytest.mark.asyncio
async def testDeleteSuccessUser(client = httpx.AsyncClient(base_url="http://0.0.0.0:8002")) -> None:
    username = "test_user_add@mail.com"
    payload = {
        "email": username,
        "password": "<hash>",
    }
    headers = {
        "Content-Type": "application/json",
    }
    testResponse = {
        "status":"User successfully removed"
    }
    response = await client.post(url="/api/v1/internal/data/remove-user", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testDeleteNotSuccessUser(client = httpx.AsyncClient(base_url="http://0.0.0.0:8002")) -> None:
    username = "test_user_add@mail.com"
    payload = {
        "email": username,
        "password": "<hash>",
    }
    headers = {
        "Content-Type": "application/json",
    }
    testResponse = {
        "status":"User removal failed, user not found"
    }
    response = await client.post(url="/api/v1/internal/data/remove-user", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == testResponse