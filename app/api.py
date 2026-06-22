from pydantic import BaseModel
from fastapi import APIRouter

from core.pipeline import Pipeline
from live.pipeline import LivePipeline
from live.events import MatchEvent, EventType

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
def start_match(data: StartMatch):
    live_pipeline.start_match(data.home, data.away)
    return {"status": "started"}


# =========================
# 推送事件
# =========================
@router.post("/event")
def push_event(event: EventIn):

    # 转换 EventType
    event_type = EventType[event.type.upper()]

    e = MatchEvent(
        minute=event.minute,
        event_type=event_type,
        team=event.team,
        player=event.player,
    )

    result = live_pipeline.step(e)

    return {
        "state": {
            "home_score": live_pipeline.state.home_score,
            "away_score": live_pipeline.state.away_score,
            "minute": live_pipeline.state.minute,
        },
        "prob": result,
    }
