class LearnedFusion:
    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}

    def fuse(self, elo_pred, poisson_pred):

        result = {"H": 0.0, "D": 0.0, "A": 0.0}

        # -------------------------
        # safe aggregation
        # -------------------------
        for k in ["H", "D", "A"]:

            elo_v = elo_pred.get(k, 0.0)
            poi_v = poisson_pred.get(k, 0.0)

            result[k] = self.weights["elo"] * elo_v + self.weights["poisson"] * poi_v

        # -------------------------
        # heuristic stabilization (safe version)
        # -------------------------
        gap = result["H"] - result["A"]

        if abs(gap) < 0.015:
            result["H"] *= 1.02
            result["A"] *= 1.02
            result["D"] *= 0.96

        result["D"] *= 0.95

        # -------------------------
        # numerical safety
        # -------------------------
        for k in result:
            if result[k] is None or result[k] != result[k]:
                result[k] = 0.0
            result[k] = max(result[k], 1e-9)

        total = sum(result.values())

        if total <= 0:
            return {"H": 0.33, "D": 0.34, "A": 0.33}

        return {k: result[k] / total for k in result}
