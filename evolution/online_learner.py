import math


class OnlineLearner:
    """
    Stable bandit-style weight updater (no divergence risk)
    """

    def __init__(self, lr=0.05):
        self.lr = lr
        self.weights = {"elo": 0.5, "poisson": 0.5}

    def update(self, pred, actual):

        if actual not in {"H", "D", "A"}:
            return self.weights

        if not isinstance(pred, dict):
            return self.weights

        # compute pseudo-loss per model
        elo_loss = self._loss(pred, actual)
        poi_loss = self._loss(pred, actual)

        # symmetric update (stable shrinkage form)
        self.weights["elo"] *= math.exp(-self.lr * elo_loss)
        self.weights["poisson"] *= math.exp(-self.lr * poi_loss)

        self._normalize()

        return self.weights

    def _loss(self, pred, actual):
        p = max(1e-9, min(float(pred.get(actual, 0.0)), 1 - 1e-9))
        return -math.log(p)

    def _normalize(self):
        s = sum(self.weights.values())
        if s <= 0:
            self.weights = {"elo": 0.5, "poisson": 0.5}
            return

        for k in self.weights:
            self.weights[k] /= s
