from locust import HttpUser, TaskSet, task, between, events
from websocket import create_connection

from uuid import uuid4


class UserBehavior(TaskSet):
    statements = [
        'Hello',
        'How are you?',
        'This chat is nice',
    ]

    def on_start(self):
        uri = "ws://localhost:8000/ws/udp-1"
        self.ws = create_connection(uri)
        self.ws.send(str(uuid4().hex))

    def on_quit(self):
        self.ws.disconnect()

    @task(1)
    def sniffer(self):
        data = self.ws.recv()
        return len(data)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 15)
