class MarketFusion:
    def __init__(self, alpha=0.7):

        # =========================
        # V1-FREEZE: alpha范围约束
        # =========================
        self.alpha = max(0.0, min(1.0, alpha))

    def fuse(self, model_prob, market_prob):

        result = {}

        for k in ["H", "D", "A"]:

            # =========================
            # V1-FREEZE: 输入安全检查
            # =========================
            if k not in model_prob or k not in market_prob:
                continue

            result[k] = self.alpha * model_prob[k] + (1 - self.alpha) * market_prob[k]

        # =========================
        # V1-FREEZE: 数值稳定性
        # =========================
        for k in result:
            result[k] = max(result[k], 1e-9)

        total = sum(result.values())

        # =========================
        # V1-FREEZE: 防止异常归一化
        # =========================
        if total <= 0:
            return {"H": 0.33, "D": 0.34, "A": 0.33}

        return {k: v / total for k, v in result.items()}
