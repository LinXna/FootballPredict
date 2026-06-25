class MarketFusion:
    def __init__(self, alpha=0.7):
        self.alpha = max(0.0, min(1.0, alpha))

    def fuse(self, model_prob, market_prob):

        result = {"H": 0.0, "D": 0.0, "A": 0.0}

        # -------------------------
        # safe merge
        # -------------------------
        for k in ["H", "D", "A"]:

            m = model_prob.get(k, 0.0)
            mk = market_prob.get(k, 0.0)

            result[k] = self.alpha * m + (1 - self.alpha) * mk

        # -------------------------
        # numerical safety
        # -------------------------
        for k in result:
            v = result[k]

            if v is None or v != v:
                v = 0.0

            result[k] = max(v, 1e-9)

        total = sum(result.values())

        if total <= 0:
            return {"H": 0.33, "D": 0.34, "A": 0.33}

        return {k: result[k] / total for k in result}
