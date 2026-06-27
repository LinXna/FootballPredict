from copy import deepcopy


class ReplayEngine:
    def __init__(self, state_store, pipeline):
        self.state_store = state_store
        self.pipeline = pipeline

    def replay(self, match_id):
        history = self.state_store.get(match_id)

        state = None
        snapshots = []

        for snap in history:
            state = deepcopy(snap.state)

            pred = self.pipeline.predict(state["home"], state["away"])

            snapshots.append(
                {"minute": snap.minute, "state": state, "prediction": pred}
            )

        return snapshots
