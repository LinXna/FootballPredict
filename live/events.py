from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


class EventType(str, Enum):
    GOAL = "goal"
    OWN_GOAL = "own_goal"

    YELLOW = "yellow_card"
    RED = "red_card"

    PENALTY = "penalty"
    SUBSTITUTION = "substitution"

    SHOT = "shot"
    SHOT_ON_TARGET = "shot_on_target"

    CORNER = "corner"
    FREE_KICK = "free_kick"
    OFFSIDE = "offside"
    FOUL = "foul"
    VAR = "var"

    PERIOD_START = "period_start"
    PERIOD_END = "period_end"

    MATCH_START = "match_start"
    MATCH_END = "match_end"

    UNKNOWN = "unknown"


@dataclass(slots=True)
class MatchEvent:
    minute: int
    event_type: EventType

    team: str | None = None
    player: str | None = None

    timestamp: datetime = field(default_factory=datetime.utcnow)
    payload: Dict[str, Any] = field(default_factory=dict)
