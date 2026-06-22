"""
live/adjuster.py

LIVE SYSTEM V1.5

实时概率调整器

职责：
    - 基于比分 + 时间调整胜率
"""

from live.state import MatchState


class LiveAdjuster:
    """
    简单动态调整模型（V1）
    """

    def __init__(self):
        # 调整强度（V1固定）
        self.k_score = 0.08
        self.k_time = 0.002

    # =========================
    # 主方法
    # =========================
    def adjust(self, prob: dict, state: MatchState) -> dict:
        """
        输入：
            prob  = {"H":x,"D":x,"A":x}
            state = MatchState

        输出：
            adjusted prob
        """

        h, a = state.home_score, state.away_score
        minute = max(1, state.minute)

        diff = h - a

        result = prob.copy()

        # =========================
        # 1️⃣ 比分影响
        # =========================
        result["H"] += diff * self.k_score
        result["A"] -= diff * self.k_score

        # =========================
        # 2️⃣ 时间影响（减少平局）
        # =========================
        decay = minute * self.k_time

        result["D"] *= max(0.2, 1 - decay)

        # =========================
        # 3️⃣ 防止概率异常
        # =========================
        for k in result:
            result[k] = max(0.01, result[k])

        # =========================
        # 4️⃣ 归一化
        # =========================
        total = sum(result.values())

        return {k: v / total for k, v in result.items()}