import asyncio
import threading
import time
from typing import List


from fastapi import WebSocket
from redis.asyncio import from_url

from app.config import settings


async def send_personal_message(message: str, websocket: WebSocket):
    await websocket.send_text(message)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.redis = from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
        self.existedConnection = False
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        if not self.existedConnection:
            self.existedConnection = True
            await self.__run_redis()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            self.active_connections.remove(websocket)
            if len(self.active_connections) == 0:
                self.existedConnection = False

    async def __broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_redis_message(self, message: str):
        await self.redis.publish("chat:c", message)

    async def __run_redis(self):
        async def listen():
            pubsub = self.redis.pubsub()
            await pubsub.psubscribe("chat:c")
            while self.existedConnection:
                async with self.lock:
                    message = await pubsub.get_message()
                    if message:
                        await self.__broadcast(str(message['data']))
                time.sleep(0.1)

        t = threading.Thread(target=asyncio.run, args=(listen(),))
        t.start()


manager = ConnectionManager()


async def get_redis_pool():
    redis = await from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    try:
        await redis.ping()
    except:
        raise SystemError('redis is not serving!')
