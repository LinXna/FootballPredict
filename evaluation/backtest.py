from evaluation.metrics import logloss, brier_score


class Backtester:
    def __init__(self, pipeline):
        # =========================
        # V1-FREEZE: 统一评估入口
        # =========================
        self.pipeline = pipeline

    def run(self, matches):

        # =========================
        # 1️⃣ 累计指标
        # =========================
        total_logloss = 0.0
        total_brier = 0.0
        correct = 0

        valid_n = 0

        # =========================
        # 2️⃣ 遍历比赛
        # =========================
        for match in matches:

            # =========================
            # V1-FREEZE: 主预测入口（不可绕过fusion）
            # =========================
            pred = self.pipeline.predict(
                match["home"], match["away"], odds=match["odds"]
            )

            actual = str(match["result"]).strip().upper()

            # =========================
            # V1-FREEZE: 数据合法性检查
            # =========================
            if not pred:
                continue

            if not all(k in pred for k in ["H", "D", "A"]):
                continue

            # =========================
            # 3️⃣ 指标计算
            # =========================
            total_logloss += logloss(pred, actual)
            total_brier += brier_score(pred, actual)

            pred_label = str(max(pred, key=pred.get)).strip().upper()

            if pred_label == actual:
                correct += 1

            valid_n += 1

        # =========================
        # 4️⃣ 防止空数据
        # =========================
        if valid_n == 0:
            return {"accuracy": 0, "logloss": 0, "brier": 0}, []

        # =========================
        # 5️⃣ 输出结果（V1锁定格式）
        # =========================
        return {
            "accuracy": correct / valid_n,
            "logloss": total_logloss / valid_n,
            "brier": total_brier / valid_n,
        }, []
