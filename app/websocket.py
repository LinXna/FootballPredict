from fastapi import APIRouter, WebSocket
from app.main import live_engine
from live.ws_adapter import handle_ws_event

router = APIRouter()

sessions = {}


@router.websocket("/ws/live")
async def ws_live(ws: WebSocket):
    await ws.accept()

    init = await ws.receive_json()
    match_id = init.get("match_id")

    while True:
        data = await ws.receive_json()
        result = handle_ws_event(live_engine, match_id, data)
        await ws.send_json(result)
