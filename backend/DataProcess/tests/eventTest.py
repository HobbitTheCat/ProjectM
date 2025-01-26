import httpx
import pytest

# @pytest.mark.asyncio
# async def testGetEvent(client=httpx.AsyncClient(base_url="http://localhost:8005")):
#     response = await client.get("/api/v1/internal/event/day?date=2025-01-24")
#     assert response.status_code == 200
#     print(response.json())

@pytest.mark.asyncio
async def testGetGroups(client=httpx.AsyncClient(base_url="http://localhost:8005")):
    response = await client.get("/api/v1/internal/event/group-list")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetGroupsWithSort(client=httpx.AsyncClient(base_url="http://localhost:8005")):
    response = await client.get("/api/v1/internal/event/group-list?sort=asc")
    assert response.status_code == 200
    data = response.json()
    print(data)
    names = [item["name"] for item in data]
    assert names == sorted(names)

    response = await client.get("/api/v1/internal/event/group-list?sort=desc")
    assert response.status_code == 200
    data = response.json()
    print(data)
    names = [item["name"] for item in data]
    assert names == sorted(names, reverse=True)

@pytest.mark.asyncio
async def testGetLocations(client=httpx.AsyncClient(base_url="http://localhost:8005")):
    response = await client.get("/api/v1/internal/event/location-list")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetTeachers(client=httpx.AsyncClient(base_url="http://localhost:8005")):
    response = await client.get("/api/v1/internal/event/teacher-list")
    assert response.status_code == 200
    print(response.json())