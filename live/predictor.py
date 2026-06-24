from live.adjuster import LiveAdjuster
from core.pipeline import Pipeline


class LivePredictor:

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        self.adjuster = LiveAdjuster()

    # =========================
    # 主入口
    # =========================
    def predict(self, state):
        """
        输入：
            MatchState

        输出：
            {"H": x, "D": x, "A": x}
        """

        # -------------------------
        # 1. 基础模型（安全调用）
        # -------------------------
        try:
            base = self.pipeline.predict(state.home, state.away)
        except Exception:
            return {"H": 0.33, "D": 0.34, "A": 0.33}

        if base is None:
            return {"H": 0.33, "D": 0.34, "A": 0.33}

        # -------------------------
        # 2. LIVE adjustment
        # -------------------------
        try:
            live_prob = self.adjuster.adjust(base, state)
        except Exception:
            live_prob = base

        # -------------------------
        # 3. 安全归一化
        # -------------------------
        try:
            total = sum(live_prob.values())

            if total <= 0:
                return {"H": 0.33, "D": 0.34, "A": 0.33}

            normalized = {k: v / total for k, v in live_prob.items()}

            return normalized

        except Exception:
            return {"H": 0.33, "D": 0.34, "A": 0.33}

    # =========================
    # 调试接口（限制风险）
    # =========================
    def predict_raw(self, state):
        try:
            return self.pipeline.predict(state.home, state.away)
        except Exception:
            return None
