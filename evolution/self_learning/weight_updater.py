class WeightUpdater:
    """
    Stable reward-weighted bandit updater
    """

    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}
        self.lr = 0.02

    def update(self, pred, actual, reward):

        if not isinstance(pred, dict):
            return self.weights

        if actual not in {0, 1, 2}:
            return self.weights

        reward = float(reward)

        # model disagreement proxy (safe version)
        probs = [
            pred.get("H", 0.0),
            pred.get("D", 0.0),
            pred.get("A", 0.0),
        ]

        probs = [max(1e-9, min(float(p), 1.0)) for p in probs]

        error = 1.0 - probs[actual]

        # stable multiplicative update (no explosion)
        self.weights["elo"] *= 1 + self.lr * reward * error
        self.weights["poisson"] *= 1 + self.lr * reward * error

        # clamp
        for k in self.weights:
            self.weights[k] = max(1e-3, self.weights[k])

        # normalize
        s = sum(self.weights.values())

        if s <= 0:
            self.weights = {"elo": 0.5, "poisson": 0.5}
            return self.weights

        self.weights = {k: v / s for k, v in self.weights.items()}

        return self.weights
