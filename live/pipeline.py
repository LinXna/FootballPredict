from copy import deepcopy

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

    # =====================================================
    # INIT MATCH
    # =====================================================
    def start_match(self, match_id: str, home: str, away: str):

        if match_id in self.store.states:
            raise ValueError(f"Match already exists: {match_id}")

        state = MatchState(home, away)

        self.store.states[match_id] = state

    # =====================================================
    # PUSH EVENT (single entry only)
    # =====================================================
    def push_event(self, match_id: str, event: MatchEvent):

        if match_id not in self.store.states:
            raise ValueError(f"Match not initialized: {match_id}")

        self.queue.push(match_id, event)

    # =====================================================
    # STEP (core runtime loop)
    # =====================================================
    def step(self, match_id: str, event: MatchEvent):

        # ensure match exists BEFORE processing
        if match_id not in self.store.states:
            raise ValueError(f"Match not initialized: {match_id}")

        # single ingestion point
        self.queue.push(match_id, event)

        state = self.store.get(match_id)

        if state is None:
            raise ValueError(f"State missing: {match_id}")

        errors = []

        # process queue
        while not self.queue.is_empty(match_id):

            e = self.queue.pop(match_id)

            try:
                state = self.processor.process(state, e)

            except Exception as ex:
                # collect error instead of silent drop
                errors.append({"event": str(e), "error": str(ex)})
                continue

        # persist updated state
        self.store.states[match_id] = state

        # snapshot for prediction (CRITICAL FIX)
        state_snapshot = deepcopy(state)

        try:
            prediction = self.predictor.predict(state_snapshot)

        except Exception:
            prediction = None

        return {"prediction": prediction, "errors": errors if errors else None}
