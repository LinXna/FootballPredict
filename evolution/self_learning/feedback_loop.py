from evolution.self_learning.reward_engine import RewardEngine


class FeedbackLoop:
    """
    将比赛结果回流到系统
    """

    def __init__(self, weight_updater):
        self.reward_engine = RewardEngine()
        self.weight_updater = weight_updater

    def process(self, pred, actual, context=None):

        reward = self.reward_engine.compute(pred, actual)

        self.weight_updater.update(pred, actual, reward)

        return reward
