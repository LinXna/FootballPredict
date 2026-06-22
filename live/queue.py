from collections import defaultdict, deque
from live.events import MatchEvent


class EventQueue:
    """
    V1.7 Multi-Match Queue
    """

    def __init__(self):
        self.queues = defaultdict(deque)

    # =========================
    # 1️⃣ 入队（按比赛）
    # =========================
    def push(self, match_id: str, event: MatchEvent):
        self.queues[match_id].append(event)

    # =========================
    # 2️⃣ 出队（按比赛）
    # =========================
    def pop(self, match_id: str):
        if not self.queues[match_id]:
            return None
        return self.queues[match_id].popleft()

    # =========================
    # 3️⃣ 判断是否为空
    # =========================
    def is_empty(self, match_id: str):
        return len(self.queues[match_id]) == 0

    # =========================
    # 4️⃣ 调试
    # =========================
    def size(self, match_id: str):
        return len(self.queues[match_id])
