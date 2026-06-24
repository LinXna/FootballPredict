from dataclasses import dataclass
from typing import Any, Dict, List
from copy import deepcopy


@dataclass
class Snapshot:
    match_id: str
    minute: int
    event: Dict[str, Any]
    state: Dict[str, Any]
    prob: Dict[str, Any]


class SnapshotStore:
    """
    V1.7 Snapshot System

    职责：
        - 记录 runtime 每一步完整状态
        - 支持 live vs replay 对比
    """

    def __init__(self):
        self._snapshots: Dict[str, List[Snapshot]] = {}

    # =========================
    # 1️⃣ 写入 snapshot
    # =========================
    def record(self, match_id: str, minute: int, event, state, prob):
        if match_id not in self._snapshots:
            self._snapshots[match_id] = []

        snap = Snapshot(
            match_id=match_id,
            minute=minute,
            event=deepcopy(event.__dict__ if hasattr(event, "__dict__") else event),
            state=deepcopy(state.__dict__ if hasattr(state, "__dict__") else state),
            prob=deepcopy(prob),
        )

        self._snapshots[match_id].append(snap)

    # =========================
    # 2️⃣ 获取全部 snapshot
    # =========================
    def get_all(self, match_id: str) -> List[Snapshot]:
        return self._snapshots.get(match_id, [])

    # =========================
    # 3️⃣ 对比一致性
    # =========================
    def compare(self, match_id: str, replay_snapshots: List[Snapshot]):
        live = self._snapshots.get(match_id, [])

        diff = []

        for l, r in zip(live, replay_snapshots):
            if l.state != r.state or l.prob != r.prob:
                diff.append({"minute": l.minute, "live": l, "replay": r})

        return diff
