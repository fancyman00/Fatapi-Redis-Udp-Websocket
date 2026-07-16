from enum import Enum


class WebSocketState(Enum):
    CONNECTING = 0
    CONNECTED = 1
    DISCONNECTED = 2
    RESPONSE = 3