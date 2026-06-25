from collections import defaultdict, deque
from typing import Optional

from live.events import MatchEvent


class EventQueue:
    """
    Safe V2 EventQueue
    """

    def __init__(self, max_size: int = 500):

        self.queues = defaultdict(deque)

        # per-match max size protection
        self.max_size = max_size

    # =====================================================
    # PUSH
    # =====================================================
    def push(self, match_id: str, event: MatchEvent):

        q = self.queues[match_id]

        q.append(event)

        # enforce bounded queue
        if len(q) > self.max_size:
            q.popleft()

    # =====================================================
    # POP (safe version)
    # =====================================================
    def pop(self, match_id: str) -> Optional[MatchEvent]:

        q = self.queues.get(match_id)

        if not q:
            return None

        try:
            return q.popleft()
        except IndexError:
            return None

    # =====================================================
    # EMPTY CHECK
    # =====================================================
    def is_empty(self, match_id: str) -> bool:

        q = self.queues.get(match_id)

        return not q or len(q) == 0

    # =====================================================
    # SIZE
    # =====================================================
    def size(self, match_id: str) -> int:

        return len(self.queues.get(match_id, []))

    # =====================================================
    # CLEANUP (important fix)
    # =====================================================
    def clear(self, match_id: str):

        if match_id in self.queues:
            del self.queues[match_id]

    # =====================================================
    # DEBUG
    # =====================================================
    def total_size(self) -> int:

        return sum(len(q) for q in self.queues.values())
