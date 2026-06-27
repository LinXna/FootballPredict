class FusionEngine:
    def fuse(self, elo, poisson):
        result = {}
        for k in ["H", "D", "A"]:
            result[k] = 0.5 * elo.get(k, 0) + 0.5 * poisson.get(k, 0)
        return self._normalize(result)

    def market_fuse(self, model, market, alpha=0.7):
        result = {}
        for k in ["H", "D", "A"]:
            result[k] = alpha * model.get(k, 0) + (1 - alpha) * market.get(k, 0)
        return self._normalize(result)

    def _normalize(self, p):
        s = sum(p.values())
        return {k: v / s for k, v in p.items()}
