from dataclasses import dataclass
from typing import Dict, List, Any
from copy import deepcopy


@dataclass
class StateSnapshot:
    minute: int
    state: Dict[str, Any]


class StateStore:
    """
    Clean V2 StateStore

    职责：
    - deterministic state ledger
    - replay support
    - evaluation support
    """

    def __init__(self):

        # match_id -> List[StateSnapshot]
        self._store: Dict[str, List[StateSnapshot]] = {}

    # =====================================================
    # APPEND STATE
    # =====================================================
    def append(self, match_id: str, minute: int, state: Any):

        if match_id not in self._store:
            self._store[match_id] = []

        snapshot = StateSnapshot(
            minute=minute,
            state=self._normalize(state),
        )

        self._store[match_id].append(snapshot)

    # =====================================================
    # NORMALIZATION (CRITICAL FIX)
    # =====================================================
    def _normalize(self, state: Any) -> Dict[str, Any]:

        if state is None:
            return {}

        if isinstance(state, dict):
            return deepcopy(state)

        if hasattr(state, "__dict__"):
            return deepcopy(state.__dict__)

        return {"value": str(state)}

    # =====================================================
    # HISTORY
    # =====================================================
    def get_history(self, match_id: str) -> List[StateSnapshot]:

        return self._store.get(match_id, [])

    # =====================================================
    # MINUTE QUERY
    # =====================================================
    def get_at_minute(self, match_id: str, minute: int):

        history = self._store.get(match_id, [])

        for snap in history:
            if snap.minute == minute:
                return snap.state

        return None

    # =====================================================
    # LATEST STATE
    # =====================================================
    def latest(self, match_id: str):

        history = self._store.get(match_id, [])

        if not history:
            return None

        return history[-1].state

    # =====================================================
    # TIMELINE (FIXED SEMANTICS)
    # =====================================================
    def get_state_timeline(self, match_id: str):

        history = self._store.get(match_id, [])

        return sorted(history, key=lambda x: x.minute)

    # =====================================================
    # CLEAR MATCH (ADDED SAFETY)
    # =====================================================
    def clear(self, match_id: str):

        if match_id in self._store:
            del self._store[match_id]
