"""
live/predictor.py

LIVE SYSTEM V1.5

实时预测输出层

职责：
    - 调用 V1 Pipeline
    - 结合 Adjuster 输出实时概率
"""

from live.adjuster import LiveAdjuster
from core.pipeline import Pipeline


class LivePredictor:
    """
    LIVE 预测核心入口
    """

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

        # =========================
        # 1️⃣ 基础模型概率（V1 Pipeline）
        # =========================
        base = self.pipeline.predict(state.home, state.away)

        # =========================
        # 2️⃣ 状态修正（LIVE调整）
        # =========================
        live_prob = self.adjuster.adjust(base, state)

        # =========================
        # 3️⃣ 返回最终概率
        # =========================
        return live_prob

    # =========================
    # 调试接口
    # =========================
    def predict_raw(self, state):
        return self.pipeline.predict(state.home, state.away)
