from typing import List, Dict, Any

from live.runtime import MatchRuntime
from live.state_store import StateStore
from live.events import MatchEvent, EventType
from live.processor import EventProcessor
from live.predictor import LivePredictor


class ReplayEngine:
    """
    V1.7 Replay Engine

    职责：
        - 从 StateStore 读取历史
        - 重建 MatchRuntime
        - 重新执行事件流
        - 输出 replay 结果
    """

    def __init__(self, state_store: StateStore, predictor: LivePredictor):
        self.state_store = state_store
        self.predictor = predictor

    # =========================
    # 1️⃣ Replay 单场比赛
    # =========================
    def replay_match(self, match_id: str):
        history = self.state_store.get_event_timeline(match_id)

        if not history:
            raise ValueError(f"No history found for match: {match_id}")

        # 重建 runtime（独立实例）
        runtime = MatchRuntime(match_id=match_id, predictor=self.predictor)

        # 初始化状态
        first_state = history[0].state
        runtime.state = first_state

        results = []

        # =========================
        # 逐条 replay
        # =========================
        for snap in history:
            state = snap.state

            # 构造“伪事件”（用于回放驱动）
            event = MatchEvent(
                minute=snap.minute,
                event_type=EventType.REPLAY,  # 特殊类型
                team="replay",
                player=None,
            )

            runtime.state = state

            prob = runtime.predict()

            results.append(
                {
                    "minute": snap.minute,
                    "state": {
                        "home_score": runtime.state.home_score,
                        "away_score": runtime.state.away_score,
                        "minute": runtime.state.minute,
                    },
                    "prob": prob,
                }
            )

        return {"match_id": match_id, "replay": results}

    # =========================
    # 2️⃣ Step-by-step Replay
    # =========================
    def replay_step(self, match_id: str, minute: int):
        history = self.state_store.get_history(match_id)

        for snap in history:
            if snap.minute == minute:
                runtime = MatchRuntime(match_id, self.predictor)
                runtime.state = snap.state

                return {
                    "minute": minute,
                    "state": runtime.state,
                    "prob": runtime.predict(),
                }

        return None
