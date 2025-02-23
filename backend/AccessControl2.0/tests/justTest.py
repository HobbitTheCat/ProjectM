import asyncio

from database.redis import get_redis, create_redis_pool, close_redis_pool

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjo0OSwidXNlcl9pZCI6OSwicmVmcmVzaCI6ZmFsc2UsImV4cCI6MTc0MDIzNjM5NX0.radaXAIu1m_uu1EaUb6A-PbCSCbz0boWmzNsiQ6tuB4"

async def redisPut():
    r = await get_redis()
    await r.set(token, "expired", ex=90)

async def redisGet():
    r = await get_redis()
    return await r.get(token)

async def main():
    await create_redis_pool()
    await redisPut()
    # print(await redisGet())
    await close_redis_pool()

# asyncio.run(main())

from routes.user import signinUser
from auth.jwt_creator import create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm


correct = OAuth2PasswordRequestForm(username='this_user_is_a_test_of_signup@accesscontrol.com', password="ThisIsATestOfSignupPassword")
asyncio.run(signinUser(correct))