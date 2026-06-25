from live.state import MatchState
from live.queue import EventQueue
from live.processor import EventProcessor
from live.predictor import LivePredictor
from live.events import MatchEvent


class MatchRuntime:
    """
    Clean V2 Runtime (NO learning side effects)
    """

    def __init__(self, match_id: str, predictor: LivePredictor):

        self.match_id = match_id

        self.state: MatchState | None = None

        self.queue = EventQueue()
        self.processor = EventProcessor()

        self.predictor = predictor

        # snapshot optional (pure dependency)
        self.snapshot_store = None

    # =====================================================
    # INIT
    # =====================================================
    def start(self, home: str, away: str):

        self.state = MatchState(home, away)

    # =====================================================
    # EVENT INGEST
    # =====================================================
    def push_event(self, event: MatchEvent):

        self.queue.push(self.match_id, event)

    # =====================================================
    # PROCESS EVENTS
    # =====================================================
    def _process_events(self):

        if self.state is None:
            raise ValueError("Match not started")

        while not self.queue.is_empty(self.match_id):

            event = self.queue.pop(self.match_id)

            if event is None:
                break

            self.state = self.processor.process(self.state, event)

    # =====================================================
    # PREDICT
    # =====================================================
    def predict(self):

        if self.state is None:
            raise ValueError("Match not started")

        return self.predictor.predict(self.state)

    # =====================================================
    # STEP (PURE RUNTIME ONLY)
    # =====================================================
    def step(self, event: MatchEvent):

        self.push_event(event)

        self._process_events()

        prob = self.predict()

        # snapshot only (NO side effects)
        if self.snapshot_store is not None:
            self.snapshot_store.record(
                self.match_id, self.state.minute, event, self.state, prob
            )

        return {
            "state": {
                "home_score": self.state.home_score,
                "away_score": self.state.away_score,
                "minute": self.state.minute,
            },
            "prob": prob,
        }

    # =====================================================
    # SNAPSHOT INJECTION
    # =====================================================
    def attach_snapshot_store(self, snapshot_store):

        self.snapshot_store = snapshot_store
