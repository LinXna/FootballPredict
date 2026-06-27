from copy import deepcopy


class LivePredictor:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def predict(self, state):
        return self.pipeline.predict(state.home, state.away)

    def safe_predict(self, state):
        try:
            return self.predict(state)
        except:
            return {"H": 0.33, "D": 0.34, "A": 0.33}
