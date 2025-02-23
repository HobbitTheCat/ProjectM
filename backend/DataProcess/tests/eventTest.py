import httpx
import pytest

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

@pytest.mark.asyncio
async def testItemByStart(client=httpx.AsyncClient(base_url="http://localhost:8005")):
    response = await client.get("/api/v1/internal/event/item-list?start=IS")
    assert response.status_code == 200
    print(response.json())


@pytest.mark.asyncio
async def testScheduleDay(client=httpx.AsyncClient(base_url="http://localhost:8005")):
    response = await client.get("/api/v1/internal/event/day")
    assert response.status_code == 422
    response = await client.get("/api/v1/internal/event/day?date=2025-01-40")
    assert response.status_code == 422
    response = await client.get("/api/v1/internal/event/day?date=2025-01-27")
    assert response.status_code == 200
    print("\ndata", response.json())
    response = await client.get('/api/v1/internal/event/day?date=2025-01-28&teacher=BAILLEUX OLIVIER')
    print("data", response.json())
    assert response.status_code == 200

@pytest.mark.asyncio
async def testScheduleWeek(client=httpx.AsyncClient(base_url="http://localhost:8005")):
    response = await client.get("/api/v1/internal/event/week")
    assert response.status_code == 422
    response = await client.get("/api/v1/internal/event/week?date=2025-01-45")
    assert response.status_code == 422
    response = await client.get("/api/v1/internal/event/week?date=2025-01-29&group=MI4-FC")
    assert response.status_code == 200
    print("\nResponse", response.json())
