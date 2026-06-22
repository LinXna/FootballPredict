"""
live/replay.py

LIVE SYSTEM V1.5

历史回放引擎（Replay Engine）

职责：
    - 重放历史事件
    - 复现 LIVE 系统行为
    - 生成预测轨迹
"""

from typing import List, Dict, Any

from live.events import MatchEvent
from live.pipeline import LivePipeline


class ReplayEngine:
    """
    用于历史比赛回放
    """

    def __init__(self, pipeline: LivePipeline):
        self.pipeline = pipeline

    # =========================
    # 主入口
    # =========================
    def run(self, events: List[MatchEvent]) -> List[Dict[str, Any]]:
        """
        输入：
            events: 历史事件列表

        输出：
            每一步的预测轨迹
        """

        outputs = []

        # =========================
        # 1️⃣ 初始化比赛（必须手动）
        # =========================
        if not events:
            return outputs

        first = events[0]
        self.pipeline.start_match(first.team or "HOME", "AWAY")

        # =========================
        # 2️⃣ 顺序回放
        # =========================
        for event in sorted(events, key=lambda e: e.minute):

            # 推入 + 处理 + 预测
            result = self.pipeline.step(event)

            outputs.append(
                {
                    "minute": event.minute,
                    "event": event.event_type.value,
                    "state": {
                        "home_score": self.pipeline.state.home_score,
                        "away_score": self.pipeline.state.away_score,
                        "minute": self.pipeline.state.minute,
                    },
                    "prob": result,
                }
            )

        return outputs
