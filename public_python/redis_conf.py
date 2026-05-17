import redis.asyncio as async_redis

from constants import REDIS_PUB_SUB_DB, REDIS_HOST, REDIS_PORT

async_redis_client = async_redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_PUB_SUB_DB, decode_responses=True
)
