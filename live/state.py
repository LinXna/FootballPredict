from dataclasses import dataclass, field
from typing import List, Any, Dict


@dataclass
class MatchState:
    match_id: str
    home: str
    away: str

    minute: int = 0
    home_score: int = 0
    away_score: int = 0
    status: str = "NS"

    events: List[Dict[str, Any]] = field(default_factory=list)

    def apply_event(self, event: dict):
        self.events.append(event)
        self.minute = max(self.minute, event.get("minute", self.minute))

        et = event.get("type")

        if et == "goal":
            team = event.get("team")
            if team == self.home:
                self.home_score += 1
            elif team == self.away:
                self.away_score += 1

    def score(self):
        return {"H": self.home_score, "A": self.away_score}

    def to_dict(self):
        return {
            "home": self.home,
            "away": self.away,
            "minute": self.minute,
            "score": self.score(),
            "status": self.status,
        }
