from copy import deepcopy

from live.runtime import MatchRuntime
from live.state_store import StateStore
from live.predictor import LivePredictor


class ReplayEngine:

    def __init__(self, state_store: StateStore, predictor: LivePredictor):

        self.state_store = state_store
        self.predictor = predictor

    # =====================================================
    # FULL MATCH REPLAY
    # =====================================================
    def replay_match(self, match_id: str):

        history = self.state_store.get_event_timeline(match_id)

        if not history:
            raise ValueError(f"No history found for match: {match_id}")

        runtime = MatchRuntime(match_id=match_id, predictor=self.predictor)

        results = []

        for snap in history:

            # IMPORTANT: avoid shared reference mutation
            state = deepcopy(snap.state)

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

    # =====================================================
    # STEP REPLAY
    # =====================================================
    def replay_step(self, match_id: str, minute: int):

        history = self.state_store.get_event_timeline(match_id)

        runtime = MatchRuntime(match_id=match_id, predictor=self.predictor)

        for snap in history:

            if snap.minute == minute:

                runtime.state = deepcopy(snap.state)

                return {
                    "minute": minute,
                    "state": {
                        "home_score": runtime.state.home_score,
                        "away_score": runtime.state.away_score,
                        "minute": runtime.state.minute,
                    },
                    "prob": runtime.predict(),
                }

        return None
