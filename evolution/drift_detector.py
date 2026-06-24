import numpy as np


class DriftDetector:
    """
    检测模型输出是否发生分布漂移
    """

    def __init__(self, window_size=50):
        self.window_size = window_size
        self.history = []

    def update(self, prob):
        self.history.append(prob)

        if len(self.history) > self.window_size:
            self.history.pop(0)

    def detect(self):
        """
        简化版 drift detection：
        计算方差变化
        """

        if len(self.history) < self.window_size:
            return False

        arr = np.array(self.history)

        var = np.var(arr, axis=0)

        # 简单阈值
        return np.mean(var) > 0.02
