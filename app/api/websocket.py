from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.schemas.websocket import WebsocketMessage
from app.services.websocket import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_redis_message(data)

    except WebSocketDisconnect:
        await manager.disconnect(websocket)


@router.get('/test/')
async def websocket_test():
    await manager.send_redis_message('123')
