"""
live/pipeline.py
LIVE SYSTEM V1.5
"""

from live.state import MatchState
from live.queue import EventQueue
from live.processor import EventProcessor
from live.predictor import LivePredictor
from live.events import MatchEvent
from live.state_store import StateStore


class LivePipeline:

    def __init__(self, core_pipeline):
        self.predictor = LivePredictor(core_pipeline)

        self.queue = EventQueue()
        self.processor = EventProcessor()

        self.store = StateStore()

    # =========================
    # 初始化比赛（统一入口）
    # =========================
    def start_match(self, match_id: str, home: str, away: str):
        state = MatchState(home, away)
        self.store.states[match_id] = state

    # =========================
    # 推送事件（match_id safe）
    # =========================
    def push_event(self, match_id: str, event: MatchEvent):
        self.queue.push(match_id, event)

    # =========================
    # step（核心实时处理）
    # =========================
    def step(self, match_id, event: MatchEvent):

        self.queue.push(match_id, event)

        state = self.store.get(match_id)

        if state is None:
            raise ValueError(f"Match not initialized: {match_id}")

        # process queue safely
        while not self.queue.is_empty(match_id):
            e = self.queue.pop(match_id)

            try:
                state = self.processor.process(state, e)
            except Exception:
                continue

        # persist state
        self.store.states[match_id] = state

        # safe predict
        try:
            return self.predictor.predict(state)
        except Exception:
            return None
