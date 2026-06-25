class Critic:

    def __init__(self):
        self.last_score = 0.0

    def evaluate(self, pred, actual):

        if not isinstance(pred, dict):
            return 0.0

        if actual not in {"H", "D", "A"}:
            return 0.0

        p = pred.get(actual, 0.0)

        # margin-aware scoring
        score = p - (1.0 - p)

        self.last_score = score

        return float(score)
