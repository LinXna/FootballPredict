class WeightManager:
    """
    Safe weight registry (validated + normalized)
    """

    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}

    def update(self, new_weights):

        if not isinstance(new_weights, dict):
            return self.weights

        cleaned = {}

        for k in ["elo", "poisson"]:
            try:
                v = float(new_weights.get(k, 0.5))
            except Exception:
                v = 0.5

            cleaned[k] = max(0.0, v)

        s = sum(cleaned.values())

        if s <= 0:
            self.weights = {"elo": 0.5, "poisson": 0.5}
            return self.weights

        self.weights = {k: v / s for k, v in cleaned.items()}

        return self.weights

    def get(self):
        return self.weights.copy()
