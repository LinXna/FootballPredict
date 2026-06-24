from dataclasses import dataclass
from typing import Dict, List, Any
from copy import deepcopy


@dataclass
class StateSnapshot:
    minute: int
    state: Any


class StateStore:
    """
    V1.7 StateStore

    职责：
        - 记录 MatchState 时间序列
        - 支持 replay
        - 支持 debug
    """

    def __init__(self):
        # match_id -> List[StateSnapshot]
        self._store: Dict[str, List[StateSnapshot]] = {}

    # =========================
    # 1️⃣ 写入状态
    # =========================
    def append(self, match_id: str, minute: int, state: Any):
        """
        追加状态快照
        """

        if match_id not in self._store:
            self._store[match_id] = []

        snapshot = StateSnapshot(minute=minute, state=deepcopy(state))

        self._store[match_id].append(snapshot)

    # =========================
    # 2️⃣ 获取完整历史
    # =========================
    def get_history(self, match_id: str) -> List[StateSnapshot]:
        return self._store.get(match_id, [])

    # =========================
    # 3️⃣ 获取某一分钟状态
    # =========================
    def get_at_minute(self, match_id: str, minute: int):
        history = self._store.get(match_id, [])

        for snap in history:
            if snap.minute == minute:
                return snap.state

        return None

    # =========================
    # 4️⃣ 获取最新状态
    # =========================
    def latest(self, match_id: str):
        history = self._store.get(match_id, [])

        if not history:
            return None

        return history[-1].state

    # =========================
    # 5️⃣ 回放支持（Replay基础）
    # =========================
    def get_event_timeline(self, match_id: str):
        """
        返回按时间排序的 state 序列
        """

        history = self._store.get(match_id, [])
        return sorted(history, key=lambda x: x.minute)
