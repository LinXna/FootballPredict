class LearnedFusion:
    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}

    def fuse(self, elo_pred, poisson_pred):

        result = {}

        for k in ["H", "D", "A"]:

            # =========================
            # V1-FREEZE: 输入安全检查
            # =========================
            if k not in elo_pred or k not in poisson_pred:
                continue

            result[k] = (
                self.weights["elo"] * elo_pred[k]
                + self.weights["poisson"] * poisson_pred[k]
            )

        # =========================
        # V1-FREEZE: 对称性修正
        # =========================
        gap = result["H"] - result["A"]

        if abs(gap) < 0.015:
            result["H"] *= 1.03
            result["A"] *= 1.03
            result["D"] *= 0.92

        # =========================
        # V1-FREEZE: D抑制（heuristic）
        # =========================
        result["D"] *= 0.92

        # =========================
        # V1-FREEZE: 数值稳定性约束
        # =========================
        for k in result:
            result[k] = max(result[k], 1e-9)

        total = sum(result.values())

        # =========================
        # V1-FREEZE: 归一化
        # =========================
        return {
            "H": result["H"] / total,
            "D": result["D"] / total,
            "A": result["A"] / total,
        }
