import asyncio
import socket
import threading


class Udp:
    def __init__(self, ip, port) -> None:
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((ip, port))

        self.thread = threading.Thread(target=asyncio.run, args=(self.worker(),))

    async def worker(self):
        pass

    def run(self):
        self.thread.start()

    def read(self) -> bytes:
        data, addr = self.__sock.recvfrom(4000)
        return data
