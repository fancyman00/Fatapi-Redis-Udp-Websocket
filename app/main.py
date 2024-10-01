from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from app.api.websocket import router as websocket_router
from app.services.telemetry import create_telemetry_service_ir

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
    ir_udp_1 = await create_telemetry_service_ir('192.168.41.28', 40004, channel='udp-1', event='ir1')
    ir_udp_1.run()
