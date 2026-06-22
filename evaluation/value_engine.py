class ValueBetEngine:
    def __init__(self, min_ev=0.02):

        # =========================
        # V1-FREEZE: EV阈值
        # =========================
        self.min_ev = min_ev

    def compute_ev(self, prob, odds):

        # =========================
        # V1-FREEZE: EV定义
        # =========================
        return prob * odds - 1

    def find_value_bets(self, pred, odds_map):

        value_bets = []

        for k in ["H", "D", "A"]:

            # =========================
            # V1-FREEZE: 输入防御
            # =========================
            if k not in pred or k not in odds_map:
                continue

            # =========================
            # V1-FREEZE: 数值稳定化
            # =========================
            p = min(max(pred[k], 1e-9), 1 - 1e-9)
            o = max(float(odds_map[k]), 1.01)

            ev = self.compute_ev(p, o)

            if ev > self.min_ev:
                value_bets.append({"outcome": k, "prob": p, "odds": o, "ev": ev})

        # =========================
        # V1-FREEZE: 排序输出
        # =========================
        return sorted(value_bets, key=lambda x: x["ev"], reverse=True)
