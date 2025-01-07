import pytest, httpx, json

@pytest.mark.asyncio
async def testWeekSchedule(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/week?date=2025-01-06")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testDaySchedule(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/day?date=2025-01-01")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListGroups(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/group-list")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListGroupsFilter(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/group-list?sort=alphabet")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListTeacher(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/teacher-list")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListTeacherFilter(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/teacher-list?sort=alphabet")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListLocation(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/location-list")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testListLocationFilter(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/event/location-list?sort=alphabet")
    assert response.status_code == 200
    print(response.json())

from models import MixedItems
test = {"items":[{"location":  "AS07"},{"teacher":  "BAILLEUX OLIVIER"},{"group": "MI4-06"}, {"group": "L2"}]}
print(MixedItems.model_validate(test))

@pytest.mark.asyncio
async def testGetFavorite(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/user/favorite-list")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testGetHistory(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    response = await client.get("/api/v1/internal/user/history-list")
    assert response.status_code == 200
    print(response.json())

@pytest.mark.asyncio
async def testPostHistory(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    with open("testData.json") as f:
        data = json.load(f)
    data = data.get("last_searched", [])

    testResponse = {
        "status": "History added successfully"
    }

    response = await client.post("/api/v1/internal/user/history", json=data)
    assert response.status_code == 200
    assert response.json() == testResponse

@pytest.mark.asyncio
async def testPostFavorite(client=httpx.AsyncClient(base_url="http://0.0.0.0:8004")) -> None:
    with open("testData.json") as f:
        data = json.load(f)
    data = data.get("favorite_list", [])
    testResponse = {
        "status": "Favorite added successfully"
    }
    response = await client.post("/api/v1/internal/user/favorite", json=data)
    assert response.status_code == 200
    assert response.json() == testResponse