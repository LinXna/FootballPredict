from live.state import MatchState
from live.events import MatchEvent, EventType


class EventProcessor:

    def __init__(self):
        # 用于简单幂等（避免重复事件）
        self._seen = set()

    # =========================
    # 单事件处理
    # =========================
    def process(self, state: MatchState, event: MatchEvent) -> MatchState:

        # -------------------------
        # 1. 幂等性保护（关键修复）
        # -------------------------
        event_key = (event.minute, event.event_type, event.team, event.player)

        if event_key in self._seen:
            return state

        self._seen.add(event_key)

        # -------------------------
        # 2. 记录事件
        # -------------------------
        state.events.append(event)

        # =========================
        # 3. 进球
        # =========================
        if event.event_type == EventType.GOAL:
            if event.team == state.home:
                state.home_score += 1
            elif event.team == state.away:
                state.away_score += 1

        # =========================
        # 4. 乌龙球（修正逻辑）
        # =========================
        elif event.event_type == EventType.OWN_GOAL:
            # 乌龙球：给对方加分（不依赖 event.team 归属）
            if event.team == state.home:
                state.away_score += 1
            elif event.team == state.away:
                state.home_score += 1

        # =========================
        # 5. 时间更新（防回退污染）
        # =========================
        if event.minute > state.minute:
            state.minute = event.minute

        # =========================
        # 6. 状态机更新（简化修复）
        # =========================
        if state.status != "FT":
            if state.minute >= 90:
                state.status = "FT"
            elif state.minute >= 45 and state.status == "1H":
                state.status = "2H"

        return state

    # =========================
    # 批量处理
    # =========================
    def process_all(self, state: MatchState, events: list[MatchEvent]) -> MatchState:

        for event in sorted(events, key=lambda e: e.minute):
            state = self.process(state, event)

        return state
