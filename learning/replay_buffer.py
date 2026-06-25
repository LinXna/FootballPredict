from collections import deque


class ReplayBuffer:

    def __init__(self, max_size=1000):
        self.buffer = deque(maxlen=max_size)

    def add(self, sample):

        if not isinstance(sample, dict):
            return

        required = ["home", "away", "result"]
        if not all(k in sample for k in required):
            return

        self.buffer.append(sample)

    def sample(self, n=32):

        n = min(n, len(self.buffer))

        return list(self.buffer)[-n:]
