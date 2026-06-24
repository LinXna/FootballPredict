from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import HTTPException

from core.pipeline import Pipeline
from live.pipeline import LivePipeline
from live.events import MatchEvent, EventType
from live.manager import LiveManager

router = APIRouter()


core_pipeline = Pipeline()
live_pipeline = LivePipeline(core_pipeline)


# =========================
# 数据模型
# =========================
class EventIn(BaseModel):
    minute: int
    type: str
    team: str
    player: str | None = None


class StartMatch(BaseModel):
    home: str
    away: str


# =========================
# 初始化比赛
# =========================
@router.post("/match/start")
def start_match(data: dict):
    return LiveManager.create_match(
        match_id=data["match_id"], home=data["home"], away=data["away"]
    )


# =========================
# 推送事件
# =========================
@router.post("/event")
def push_event(data: dict):
    event = MatchEvent(
        minute=data["minute"],
        event_type=EventType[data["type"].upper()],
        team=data["team"],
        player=data.get("player"),
    )

    return LiveManager.handle_event(match_id=data["match_id"], event=event)
