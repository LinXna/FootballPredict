import math


class RewardEngine:

    def compute(self, pred, actual):

        p = float(pred.get(actual, 0.0))
        p = max(1e-9, min(p, 1 - 1e-9))

        return math.log(p)
