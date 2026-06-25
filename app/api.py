from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from core.pipeline import Pipeline
from live.pipeline import LivePipeline
from live.events import MatchEvent, EventType
from live.manager import LiveManager

router = APIRouter()

# -------------------------
# lazy init (fix global state issue)
# -------------------------
core_pipeline = None
live_pipeline = None


def get_live():
    global core_pipeline, live_pipeline
    if core_pipeline is None:
        core_pipeline = Pipeline()
        live_pipeline = LivePipeline(core_pipeline)
    return live_pipeline


# =========================
# Models
# =========================


class StartMatch(BaseModel):
    match_id: str
    home: str
    away: str


class EventIn(BaseModel):
    match_id: str
    minute: int
    type: str
    team: str
    player: str | None = None


# =========================
# Start match
# =========================
@router.post("/match/start")
def start_match(data: StartMatch):
    try:
        live = get_live()
        return LiveManager.create_match(
            match_id=data.match_id, home=data.home, away=data.away
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"start_match failed: {e}")


# =========================
# Push event
# =========================
@router.post("/event")
def push_event(data: EventIn):

    try:
        live = get_live()

        # safe enum conversion
        try:
            event_type = EventType[data.type.upper()]
        except Exception:
            raise HTTPException(
                status_code=400, detail=f"Invalid event type: {data.type}"
            )

        event = MatchEvent(
            minute=data.minute,
            event_type=event_type,
            team=data.team,
            player=data.player,
        )

        return LiveManager.handle_event(match_id=data.match_id, event=event)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"push_event failed: {e}")
