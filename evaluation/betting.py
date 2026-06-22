class BettingEngine:
    def __init__(self, bankroll=1000):

        # =========================
        # V1-FREEZE: bankroll初始化
        # =========================
        self.bankroll = bankroll
        self.init = bankroll

    def kelly(self, p, odds):

        b = odds - 1

        # =========================
        # V1-FREEZE: 防止非法赔率
        # =========================
        if b <= 0:
            return 0

        q = 1 - p
        return max(0, (b * p - q) / b)

    def run(self, matches, pipeline):

        for m in matches:

            # =========================
            # V1-FREEZE: 统一预测入口
            # =========================
            pred = pipeline.predict(m["home"], m["away"], odds=m["odds"])

            if not pred:
                continue

            if not all(k in pred for k in ["H", "D", "A"]):
                continue

            best = max(pred, key=pred.get)

            # =========================
            # V1-FREEZE: 概率裁剪
            # =========================
            p = max(0.0001, min(0.9999, pred[best]))

            # =========================
            # V1-FREEZE: odds安全读取
            # =========================
            o = float(m["odds"].get(best, 2.0))
            o = max(o, 1.01)

            f = self.kelly(p, o)

            stake = self.bankroll * f

            # =========================
            # V1-FREEZE: 风险控制（10% cap）
            # =========================
            stake = min(stake, self.bankroll * 0.1)

            if m["result"] == best:
                self.bankroll += stake * (o - 1)
            else:
                self.bankroll -= stake

            # =========================
            # V1-FREEZE: 防止负值爆炸
            # =========================
            self.bankroll = max(0, self.bankroll)

        return {
            "ROI": (self.bankroll - self.init) / self.init,
            "final_bankroll": self.bankroll,
        }
