import os
from redis.asyncio import Redis, from_url
from dotenv import load_dotenv
load_dotenv()

redisPath = os.getenv('REDIS_PATH')
redis_pool: Redis = None

async def create_redis_pool():
    global redis_pool
    redis_pool = from_url(redisPath, max_connections=10)

async def close_redis_pool():
    await redis_pool.close()

async def get_redis()->Redis:
    return redis_pool