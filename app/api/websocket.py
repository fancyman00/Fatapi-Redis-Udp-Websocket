from fastapi import APIRouter, WebSocket, Depends
from redis.asyncio import Redis

from app.services.websocket import worker
from app.services.redis import get_redis

router = APIRouter()


@router.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, redis: Redis = Depends(get_redis), channel: str = '*'):
    await worker(websocket, redis, channel)


@router.get('/test/{channel}')
async def websocket_test(redis: Redis = Depends(get_redis), channel: str = '*'):
    print(await redis.publish(channel, '123'))
