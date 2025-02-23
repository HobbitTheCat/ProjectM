import pytest
import httpx

baseUrl = "http://localhost:8005"

@pytest.mark.asyncio
async def testInternalTest(client=httpx.AsyncClient(base_url=baseUrl)):
    payload = {
        "name": "MI4-FC",
        "type": "Group"
    }
    response = await client.post("/api/v1/internal/check-item", json=payload)
    assert response.status_code == 200

@pytest.mark.asyncio
async def testInternalTest1(client=httpx.AsyncClient(base_url=baseUrl)):
    payload = {
        "name": "MI4-FO",
        "type": "Group"
    }
    response = await client.post("/api/v1/internal/check-item", json=payload)
    assert response.status_code == 404
