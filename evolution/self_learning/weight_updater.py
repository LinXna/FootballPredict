class WeightUpdater:
    """
    更新 Elo / Poisson / Fusion 权重
    """

    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}

        self.lr = 0.02

    def update(self, pred, actual, reward):

        target = [0, 0, 0]
        target[actual] = 1

        error_h = target[0] - pred["H"]
        error_d = target[1] - pred["D"]
        error_a = target[2] - pred["A"]

        avg_error = (error_h + error_d + error_a) / 3

        # reward-driven update
        self.weights["elo"] += self.lr * reward * avg_error
        self.weights["poisson"] += self.lr * reward * avg_error

        # normalize
        s = sum(self.weights.values())
        for k in self.weights:
            self.weights[k] /= s
