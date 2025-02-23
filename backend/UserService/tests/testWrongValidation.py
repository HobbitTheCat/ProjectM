import pytest, httpx

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo1MjU2MDAsInVzZXJfaWQiOjEsInJlZnJlc2giOmZhbHNlLCJleHAiOjE3Mzk0NjUwMTZ9.MtNUdHz3JKpxfX7NV5fzvQaRMdHj68wZopyGsvv3_h8"
address = "http://0.0.0.0:8006"

headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
}

@pytest.mark.asyncio
async def testUserUpdateGroup(client=httpx.AsyncClient(base_url=address)):
    payload = {"name": "A108"}
    response = await client.put("/api/v1/internal/user/group", headers=headers, json=payload)
    assert response.status_code == 404