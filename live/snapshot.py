from dataclasses import dataclass
from typing import Any, Dict, List
from copy import deepcopy


@dataclass
class Snapshot:
    match_id: str
    minute: int

    # strictly normalized payloads
    event: Dict[str, Any]
    state: Dict[str, Any]
    prob: Dict[str, Any]


class SnapshotStore:
    """
    Clean V2 Snapshot System

    目标：
    - deterministic replay
    - stable evaluation
    - no hidden learning coupling
    """

    def __init__(self):
        self._snapshots: Dict[str, List[Snapshot]] = {}

    # =====================================================
    # RECORD SNAPSHOT (safe normalization)
    # =====================================================
    def record(self, match_id: str, minute: int, event, state, prob):

        if match_id not in self._snapshots:
            self._snapshots[match_id] = []

        snap = Snapshot(
            match_id=match_id,
            minute=minute,
            event=self._normalize(event),
            state=self._normalize(state),
            prob=deepcopy(prob),
        )

        self._snapshots[match_id].append(snap)

    # =====================================================
    # NORMALIZATION (CRITICAL FIX)
    # =====================================================
    def _normalize(self, obj):

        if obj is None:
            return {}

        # dataclass
        if hasattr(obj, "__dict__"):
            return deepcopy(obj.__dict__)

        # dict
        if isinstance(obj, dict):
            return deepcopy(obj)

        # fallback safe cast
        return {"value": str(obj)}

    # =====================================================
    # GET ALL
    # =====================================================
    def get_all(self, match_id: str) -> List[Snapshot]:

        return self._snapshots.get(match_id, [])

    # =====================================================
    # CONSISTENCY COMPARE (improved)
    # =====================================================
    def compare(self, match_id: str, replay_snapshots: List[Snapshot]):

        live = self._snapshots.get(match_id, [])

        diff = []

        for l, r in zip(live, replay_snapshots):

            if self._diff(l.state, r.state) or self._diff(l.prob, r.prob):
                diff.append({"minute": l.minute, "live": l, "replay": r})

        return diff

    # =====================================================
    # DEEP SAFE DIFF
    # =====================================================
    def _diff(self, a: Dict[str, Any], b: Dict[str, Any]) -> bool:

        if a.keys() != b.keys():
            return True

        for k in a:
            if isinstance(a[k], float) and isinstance(b[k], float):
                if abs(a[k] - b[k]) > 1e-6:
                    return True
            else:
                if a[k] != b[k]:
                    return True

        return False
