from evolution.self_learning.reward_engine import RewardEngine


class FeedbackLoop:
    """
    Safe feedback controller
    """

    def __init__(self, weight_updater):
        self.reward_engine = RewardEngine()
        self.weight_updater = weight_updater

    def process(self, pred, actual, context=None):

        if not isinstance(pred, dict):
            return 0.0

        if actual not in {0, 1, 2}:
            return 0.0

        try:
            reward = self.reward_engine.compute(pred, actual)

            # safety clamp
            reward = max(-1.0, min(1.0, float(reward)))

            self.weight_updater.update(pred, actual, reward)

            return reward

        except Exception:
            return 0.0
