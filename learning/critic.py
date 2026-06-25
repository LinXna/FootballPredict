class ModelCritic:
    """
    Evaluates model quality over time
    """

    def score(self, history):

        if not history:
            return 0.5

        correct = sum(1 for h in history if h["correct"])
        return correct / len(history)
