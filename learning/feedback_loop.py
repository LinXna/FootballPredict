class FeedbackLoop:
    def __init__(self, learner):
        self.learner = learner

    def process(self, pred, actual):
        self.learner.update(pred, actual)

        return {"updated_weights": self.learner.weights}
