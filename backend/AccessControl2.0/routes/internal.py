import httpx, os
from dotenv import load_dotenv
load_dotenv()

user_url = os.getenv("USER_URL_CREATE")
user_info_url = os.getenv("USER_URL_INFO")


async def notify_user_service(username:str,uid:int):
    payload = {
        "uid": uid,
        "username": username,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url=user_url, json=payload)
        response.raise_for_status()

async def get_user_info(token:str):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(url=user_info_url, headers=headers)
        response.raise_for_status()
    return response.json()

async def delete_user_service(token:str):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.delete(url=user_url, headers=headers)
        response.raise_for_status()