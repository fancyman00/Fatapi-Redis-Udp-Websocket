import asyncio

from fastapi import APIRouter, WebSocket, Depends
from redis.asyncio import Redis

from app.services.websocket import get_redis, listen_redis, listen_socket, channel

router = APIRouter()


@router.websocket("/ws/{used_id}")
async def websocket_endpoint(websocket: WebSocket, redis: Redis = Depends(get_redis), ):

    await websocket.accept()

    try:
        await asyncio.gather(
            listen_socket(websocket, redis),
            listen_redis(websocket, redis)
        )
    except Exception as e:
        print(f"Error in websocket_endpoint: {e}")
    finally:
        await redis.close()  # Закрываем соединение с Redis
        print('Redis connection closed')


@router.get('/test/')
async def websocket_test(redis: Redis = Depends(get_redis)):
    print(await redis.publish(channel, '123'))
