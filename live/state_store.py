from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class Snapshot:
    minute: int
    state: Dict[str, Any]
    pred: Dict[str, Any]


class StateStore:
    def __init__(self):
        self.store = {}

    def record(self, match_id, state, pred):
        self.store.setdefault(match_id, []).append(
            Snapshot(minute=state.minute, state=state.to_dict(), pred=pred)
        )

    def get(self, match_id):
        return self.store.get(match_id, [])
