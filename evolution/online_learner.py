class OnlineLearner:
    """
    基于比赛结果进行轻量权重调整
    """

    def __init__(self):
        self.lr = 0.01
        self.weights = {"elo": 0.5, "poisson": 0.5}

    def update(self, pred, actual):
        """
        pred: {"H":, "D":, "A":}
        actual: result index (0/1/2)
        """

        target = [0, 0, 0]
        target[actual] = 1

        for i, key in enumerate(["H", "D", "A"]):
            error = target[i] - pred[key]

            self.weights["elo"] += self.lr * error
            self.weights["poisson"] += self.lr * error

        # normalize
        s = sum(self.weights.values())
        for k in self.weights:
            self.weights[k] /= s
