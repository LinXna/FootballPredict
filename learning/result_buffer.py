from collections import deque


class ResultBuffer:
    """
    保存最近N场比赛结果
    防止单场比赛立即更新权重
    """

    def __init__(self, max_size=50):
        self.buffer = deque(maxlen=max_size)

    def add(self, sample):
        self.buffer.append(sample)

    def ready(self):
        return len(self.buffer) >= 20

    def samples(self):
        return list(self.buffer)

    def clear(self):
        self.buffer.clear()

    def __len__(self):
        return len(self.buffer)
