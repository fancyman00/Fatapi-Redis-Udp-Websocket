import asyncio
import socket
import threading
from app.services.websocket import manager


class UdpManager:
    def __init__(self, ip, port, handler) -> None:
        self.handler=handler
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((ip, port))
        self.thread = threading.Thread(target=asyncio.run, args=(self.worker(), ))
        self.thread.start()
    
    async def worker(self):
        while True:
            data, addr = self.__sock.recvfrom(4000)
            await self.handler(str(data))
