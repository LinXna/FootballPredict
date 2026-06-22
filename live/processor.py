"""
live/processor.py

LIVE SYSTEM V1.5

事件处理器（核心引擎）

职责：
    - 接收 MatchEvent
    - 更新 MatchState
"""

from live.state import MatchState
from live.events import MatchEvent, EventType


class EventProcessor:
    """
    将事件应用到比赛状态
    """

    def __init__(self):
        pass

    # =========================
    # 主入口
    # =========================
    def process(self, state: MatchState, event: MatchEvent) -> MatchState:
        """
        应用单个事件到状态
        """

        # 记录事件
        state.events.append(event)

        # =========================
        # 1️⃣ 进球
        # =========================
        if event.event_type == EventType.GOAL:
            if event.team == state.home:
                state.home_score += 1
            elif event.team == state.away:
                state.away_score += 1

        # =========================
        # 2️⃣ 乌龙球
        # =========================
        elif event.event_type == EventType.OWN_GOAL:
            if event.team == state.home:
                state.away_score += 1
            elif event.team == state.away:
                state.home_score += 1

        # =========================
        # 3️⃣ 时间更新
        # =========================
        if event.minute >= state.minute:
            state.minute = event.minute

        # =========================
        # 4️⃣ 比赛阶段更新（简化版）
        # =========================
        if state.minute >= 90:
            state.status = "FT"
        elif state.minute >= 45 and state.status == "1H":
            state.status = "2H"

        return state

    # =========================
    # 批量处理
    # =========================
    def process_all(self, state: MatchState, events: list[MatchEvent]) -> MatchState:
        """
        顺序处理多个事件
        """

        for event in sorted(events, key=lambda e: e.minute):
            state = self.process(state, event)

        return state
