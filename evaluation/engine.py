import math


class EvaluationEngine:
    def __init__(self):
        self.results = []

    def evaluate_match(self, pred, actual):
        pred = self._normalize(pred)

        logloss = -math.log(max(1e-9, pred.get(actual, 1e-9)))
        brier = self._brier(pred, actual)

        correct = int(max(pred, key=pred.get) == actual)

        self.results.append({"logloss": logloss, "brier": brier, "correct": correct})

        return logloss, brier, correct

    def summary(self):
        n = len(self.results)
        if n == 0:
            return {}

        return {
            "logloss": sum(r["logloss"] for r in self.results) / n,
            "brier": sum(r["brier"] for r in self.results) / n,
            "accuracy": sum(r["correct"] for r in self.results) / n,
        }

    def _brier(self, pred, actual):
        return sum((p - (k == actual)) ** 2 for k, p in pred.items())

    def _normalize(self, p):
        s = sum(p.values())
        return {k: v / s for k, v in p.items()}
