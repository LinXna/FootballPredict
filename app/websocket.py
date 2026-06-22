from fastapi import APIRouter, WebSocket
from core.pipeline import Pipeline
from live.pipeline import LivePipeline
from live.events import MatchEvent, EventType

router = APIRouter()

core_pipeline = Pipeline()
live_pipeline = LivePipeline(core_pipeline)


@router.websocket("/ws/live/{match_id}")
async def live(ws: WebSocket, match_id: str):
    await ws.accept()

    await ws.send_json({"status": "connected", "match_id": match_id})

    live_pipeline.start_match(match_id, "Brazil", "France")

    while True:
        try:
            data = await ws.receive_json()

            event = MatchEvent(
                minute=data["minute"],
                event_type=EventType[data["type"].upper()],
                team=data["team"],
                player=data.get("player"),
            )

            state = live_pipeline.store.get(match_id)
            result = live_pipeline.step(match_id, event)

            await ws.send_json({"state": state.to_dict(), "prob": result})

        except Exception as e:
            await ws.send_json({"error": str(e)})
            break
