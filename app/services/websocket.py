from fastapi import WebSocket
from redis.asyncio import from_url, Redis

from app.config import settings
from app.model.websocket import WebSocketState

channel = 'user:channel'


async def listen_socket(websocket: WebSocket, redis: Redis):
    while True:
        try:
            data = await websocket.receive_text()
            await redis.publish(channel, data)
        except Exception as e:
            print(f"Error in listen_socket: {e}")
            await redis.publish(channel, 'disconnect_user')
            break


async def listen_redis(websocket: WebSocket, redis: Redis):
    ps = redis.pubsub()
    await ps.psubscribe(channel)

    try:
        async for message in ps.listen():
            if message['type'] == 'pmessage':
                if websocket.client_state == WebSocketState.CONNECTED:
                    try:
                        await websocket.send_text(message['data'])
                    except Exception as e:
                        print(f"Error sending message to WebSocket: {e}")
                        break
    finally:
        await ps.punsubscribe(channel)
        if websocket.client_state == WebSocketState.CONNECTED:
            await websocket.close()
        print('Exited redis listener and closed WebSocket')


async def get_redis():
    return await from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
