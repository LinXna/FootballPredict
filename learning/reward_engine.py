import math


class RewardEngine:

    def compute(self, pred, actual):

        if not isinstance(pred, dict):
            return 0.0

        if actual not in {"H", "D", "A"}:
            return 0.0

        p = float(pred.get(actual, 0.0))
        p = max(1e-9, min(p, 1 - 1e-9))

        # proper scoring rule (log reward)
        reward = math.log(p)

        return float(reward)
