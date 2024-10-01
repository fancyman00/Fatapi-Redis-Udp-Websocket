import asyncio

from fastapi import WebSocket
from redis.asyncio import Redis


async def worker(websocket: WebSocket, redis: Redis, channel: str):
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

