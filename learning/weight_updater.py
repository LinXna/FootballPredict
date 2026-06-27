class WeightUpdater:

    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}

    def update(self, pred, actual, reward):

        p = float(pred.get(actual, 0.0))
        error = 1.0 - p

        for k in self.weights:
            self.weights[k] += reward * error

    def get(self):
        return self.weights
