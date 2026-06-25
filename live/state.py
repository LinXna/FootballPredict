from dataclasses import dataclass, field
from typing import List, Any, Dict
from copy import deepcopy


@dataclass
class MatchState:
    """
    Stable V2 MatchState

    目标：
    - deterministic snapshot
    - safe serialization
    - no external mutation leak
    """

    # =========================
    # basic info
    # =========================
    home: str
    away: str

    # =========================
    # match state
    # =========================
    minute: int = 0
    status: str = "NS"  # NS / 1H / HT / 2H / ET / FT

    # =========================
    # score
    # =========================
    home_score: int = 0
    away_score: int = 0

    # =========================
    # events (protected)
    # =========================
    events: List[Any] = field(default_factory=list)

    # =====================================================
    # SCORE
    # =====================================================
    @property
    def score(self) -> str:
        return f"{self.home_score}-{self.away_score}"

    # =====================================================
    # FINISHED
    # =====================================================
    def is_finished(self) -> bool:
        return self.status == "FT"

    # =====================================================
    # RESET
    # =====================================================
    def reset(self) -> None:
        self.minute = 0
        self.status = "NS"
        self.home_score = 0
        self.away_score = 0
        self.events.clear()

    # =====================================================
    # SAFE SERIALIZATION (CRITICAL FIX)
    # =====================================================
    def to_dict(self) -> Dict[str, Any]:

        return {
            "home": self.home,
            "away": self.away,
            "minute": self.minute,
            "status": self.status,
            "home_score": self.home_score,
            "away_score": self.away_score,
            "events": deepcopy(self.events),
        }

    # =====================================================
    # SAFE EVENT ACCESS
    # =====================================================
    def get_events(self) -> List[Any]:
        return list(self.events)

    # =====================================================
    # STRING
    # =====================================================
    def __str__(self) -> str:
        return (
            f"[{self.status}] "
            f"{self.home} "
            f"{self.home_score}-{self.away_score} "
            f"{self.away} "
            f"({self.minute}')"
        )
