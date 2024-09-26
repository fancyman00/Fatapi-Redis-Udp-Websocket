from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.websocket import router as websocket_router
from app.services.udp import UdpManager
from app.services.websocket import get_redis_pool
from app.services.websocket import manager

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router)


@app.on_event("startup")
async def startup_event():
    await get_redis_pool()
    UdpManager('192.168.41.28', 40004, manager.send_redis_message)
