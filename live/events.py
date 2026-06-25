from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict


# =========================================================
# EventType（保持原结构，但增强语义约束）
# =========================================================
class EventType(str, Enum):
    """比赛事件类型（稳定版）"""

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


# =========================================================
# MatchEvent（增强安全 + schema约束）
# =========================================================
@dataclass(slots=True)
class MatchEvent:
    """
    LIVE事件对象（安全增强版）

    核心改动：
    - payload schema filter
    - safe normalization
    - downstream isolation ready
    """

    minute: int
    event_type: EventType

    team: str | None = None
    player: str | None = None

    timestamp: datetime = field(default_factory=datetime.utcnow)

    payload: Dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # 安全控制字段（新增）
    # =====================================================
    _SAFE_PAYLOAD_KEYS = {
        "xg",
        "assist",
        "shot_type",
        "card_reason",
        "var_decision",
        "position",
        "distance",
    }

    def __post_init__(self):

        # -----------------------------
        # 1. minute safety
        # -----------------------------
        if not isinstance(self.minute, int) or self.minute < 0:
            self.minute = 0

        # -----------------------------
        # 2. team/player normalization
        # -----------------------------
        if self.team is not None and not isinstance(self.team, str):
            self.team = str(self.team)

        if self.player is not None and not isinstance(self.player, str):
            self.player = str(self.player)

        # -----------------------------
        # 3. payload sanitization (关键修复点)
        # -----------------------------
        self.payload = self._sanitize_payload(self.payload)

    # =====================================================
    # payload 安全过滤（核心修复）
    # =====================================================
    def _sanitize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        if not isinstance(payload, dict):
            return {}

        safe = {}

        for k, v in payload.items():

            # 只允许白名单字段
            if k not in self._SAFE_PAYLOAD_KEYS:
                continue

            # 防止嵌套污染
            if isinstance(v, dict) or isinstance(v, list):
                continue

            safe[k] = v

        return safe

    # =====================================================
    # debug / display
    # =====================================================
    def __str__(self) -> str:

        return (
            f"[{self.minute}'] "
            f"{self.event_type.value} "
            f"{self.team or ''} "
            f"{self.player or ''}"
        )

    # =====================================================
    # semantic helpers
    # =====================================================
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
