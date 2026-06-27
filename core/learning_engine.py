class LearningEngine:
    def __init__(self, lr=0.05):
        self.lr = lr
        self.weights = {"H": 1.0, "D": 1.0, "A": 1.0}

    def update(self, pred, actual):
        pred = self._clip(pred)

        error = {}
        for k in self.weights:
            target = 1.0 if k == actual else 0.0
            error[k] = target - pred.get(k, 0.0)

        for k in self.weights:
            self.weights[k] += self.lr * error[k]

        self._normalize()

    def apply(self, pred):
        return {k: pred.get(k, 0.0) * self.weights.get(k, 1.0) for k in pred}

    def _normalize(self):
        s = sum(self.weights.values())
        for k in self.weights:
            self.weights[k] /= s

    def _clip(self, p):
        return {k: max(1e-9, min(v, 1 - 1e-9)) for k, v in p.items()}
