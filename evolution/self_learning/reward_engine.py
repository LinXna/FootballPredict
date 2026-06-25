class RewardEngine:
    """
    Proper scoring reward (log-loss based stable version)
    """

    def compute(self, pred, actual):

        try:
            probs = [
                float(pred.get("H", 0)),
                float(pred.get("D", 0)),
                float(pred.get("A", 0)),
            ]
        except Exception:
            return 0.0

        # clamp probabilities
        probs = [max(1e-9, min(p, 1 - 1e-9)) for p in probs]

        # normalize safety
        s = sum(probs)
        if s <= 0:
            return 0.0

        probs = [p / s for p in probs]

        # log-loss style reward
        p = probs[actual]

        return -(-1.0 * (1.0 * (1 - p)))
