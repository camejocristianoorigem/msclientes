import json
import os
import redis.asyncio as redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = None

async def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
        socket_timeout=2.0
    )

async def init_redis():
    global redis_client
    redis_client = await get_redis_client()

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()

async def get_cache(key: str):
    try:
        client = await get_redis_client()
        data = await client.get(key)
        await client.close()
        return json.loads(data) if data else None
    except Exception:
        return None

async def set_cache(key: str, value: dict, ttl: int = 300):
    try:
        client = await get_redis_client()
        await client.set(key, json.dumps(value), ex=ttl)
        await client.close()
    except Exception:
        pass

async def delete_cache(key: str):
    try:
        client = await get_redis_client()
        await client.delete(key)
        await client.close()
    except Exception:
        pass
