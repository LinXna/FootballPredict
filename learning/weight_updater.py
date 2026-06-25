import math


class WeightUpdater:

    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}
        self.lr = 0.03

    def update(self, pred, actual, reward):

        if not isinstance(pred, dict):
            return self.weights

        if actual not in {"H", "D", "A"}:
            return self.weights

        reward = float(reward)

        p = max(1e-9, min(float(pred.get(actual, 0.0)), 1 - 1e-9))

        error = 1.0 - p

        # stable exponential update
        self.weights["elo"] *= math.exp(self.lr * reward * error)
        self.weights["poisson"] *= math.exp(self.lr * reward * error)

        # normalize
        s = sum(self.weights.values())

        if s <= 0:
            self.weights = {"elo": 0.5, "poisson": 0.5}
            return self.weights

        self.weights = {k: v / s for k, v in self.weights.items()}

        return self.weights
