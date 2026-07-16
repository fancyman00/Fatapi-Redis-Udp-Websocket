from redis.asyncio import from_url
from app.config import settings


async def get_redis():
    return await from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
