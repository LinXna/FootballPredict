from copy import deepcopy
from live.state import MatchState
from live.queue import EventQueue
from core.learning_engine import LearningEngine


class LiveEngine:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.queue = EventQueue()
        self.state_store = {}

        # V2.1 learning hook
        self.learner = LearningEngine()

    def start_match(self, match_id, home, away):
        self.state_store[match_id] = MatchState(match_id=match_id, home=home, away=away)

    def push_event(self, match_id, event):
        self.queue.push(match_id, event)
        return self.step(match_id)

    def step(self, match_id):
        state = self.state_store.get(match_id)
        if not state:
            return None

        event = self.queue.pop(match_id)
        if not event:
            return state.to_dict()

        state.apply_event(event)

        pred = self.pipeline.predict(state.home, state.away)

        # apply learning adjustment
        adjusted = self.learner.apply(pred)

        return {
            "state": state.to_dict(),
            "prediction": adjusted,
            "weights": self.learner.weights,
        }

    def get_state(self, match_id):
        state = self.state_store.get(match_id)
        return state.to_dict() if state else None
