from collections import defaultdict, deque


class EventQueue:
    def __init__(self):
        self.q = defaultdict(deque)

    def push(self, match_id, event):
        self.q[match_id].append(event)

    def pop(self, match_id):
        if self.q[match_id]:
            return self.q[match_id].popleft()
        return None

    def empty(self, match_id):
        return len(self.q[match_id]) == 0
