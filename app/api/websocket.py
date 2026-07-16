from fastapi import APIRouter, WebSocket, Depends
from redis.asyncio import Redis
import asyncio
from app.services.redis import get_redis

router = APIRouter()


@router.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, redis: Redis = Depends(get_redis), channel: str = '*'):
    await websocket.accept()

    ps = redis.pubsub()

    async def listen_socket():
        while True:
            try:
                await websocket.receive_text()
            except Exception as e:
                raise Exception(f"Error in listen_socket: {e}")

    async def listen_redis():
        await ps.psubscribe(channel)
        try:
            async for message in ps.listen():
                if message['type'] == 'pmessage':
                    await websocket.send_text(message['data'])
        except Exception as e:
            raise Exception(f"Error in listen_redis: {e}")

    try:
        tasks = [listen_socket(), listen_redis()]
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error in websocket_endpoint: {e}")
    finally:
        await ps.punsubscribe(channel)
        await redis.close()
        await redis.close()
        print('Connection closed')


@router.get('/test/{channel}')
async def websocket_test(redis: Redis = Depends(get_redis), channel: str = '*'):
    await redis.publish(channel, '123')
