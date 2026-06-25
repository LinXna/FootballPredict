from learning.reward_engine import RewardEngine


class Feedback:

    def __init__(self, updater):
        self.reward_engine = RewardEngine()
        self.updater = updater

    def process(self, pred, actual):

        reward = self.reward_engine.compute(pred, actual)

        reward = max(-1.0, min(1.0, reward))

        self.updater.update(pred, actual, reward)

        return reward
