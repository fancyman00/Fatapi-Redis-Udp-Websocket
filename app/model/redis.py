from redis.asyncio import Redis
from app.model.base import Udp


class UdpRedis(Udp):
    redis = None

    def __init__(self, ip, port, channel):
        super().__init__(ip, port)
        self.channel = channel

    def init(self, redis):
        self.redis = redis

    def get_message(self) -> str:
        data = self.read()
        return str(data)

    async def worker(self):
        while True:
            if self.redis:
                await self.redis.publish(channel=self.channel, message=self.get_message())
