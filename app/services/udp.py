import asyncio
import socket
import threading
from app.services.redis import get_redis


class UdpManager:
    def __init__(self, ip, port, channel) -> None:
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((ip, port))
        self.thread = threading.Thread(target=asyncio.run, args=(self.worker(),))
        self.channel = channel
        self.thread.start()

    async def worker(self):
        redis = await get_redis()
        while True:
            data, addr = self.__sock.recvfrom(4000)
            await redis.publish(channel=self.channel, message=str(data))
