from collections import deque


class ResultBuffer:

    def __init__(self, max_size=500):
        self.buffer = deque(maxlen=max_size)

    def push(self, result):

        if not isinstance(result, dict):
            return

        if "pred" not in result or "actual" not in result:
            return

        self.buffer.append(result)

    def get_all(self):
        return list(self.buffer)
