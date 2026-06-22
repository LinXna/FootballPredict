from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict


class EventType(str, Enum):
    """比赛事件类型"""

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
    """
    LIVE事件对象
    """

    minute: int

    event_type: EventType

    team: str | None = None

    player: str | None = None

    timestamp: datetime = field(default_factory=datetime.utcnow)

    payload: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return (
            f"[{self.minute}'] "
            f"{self.event_type.value} "
            f"{self.team or ''} "
            f"{self.player or ''}"
        )

    @property
    def is_goal(self) -> bool:
        return self.event_type in (
            EventType.GOAL,
            EventType.OWN_GOAL,
        )

    @property
    def is_red(self) -> bool:
        return self.event_type == EventType.RED

    @property
    def is_yellow(self) -> bool:
        return self.event_type == EventType.YELLOW
