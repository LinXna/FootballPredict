import numpy as np


class DriftDetector:
    """
    KL-approx drift detector (stable version)
    """

    def __init__(self, window_size=50):
        self.window_size = window_size
        self.history = []

    def update(self, prob):
        if not isinstance(prob, dict):
            return

        vec = self._to_vector(prob)
        if vec is None:
            return

        self.history.append(vec)

        if len(self.history) > self.window_size:
            self.history.pop(0)

    def detect(self):

        if len(self.history) < self.window_size:
            return False

        arr = np.array(self.history)

        mean = np.mean(arr, axis=0)
        var = np.var(arr, axis=0)

        # normalized variance drift score
        score = np.mean(var / (mean + 1e-9))

        return score > 0.15

    def _to_vector(self, prob):
        try:
            return np.array(
                [
                    float(prob.get("H", 0)),
                    float(prob.get("D", 0)),
                    float(prob.get("A", 0)),
                ]
            )
        except Exception:
            return None
