class LearningEngine:

    def __init__(self, weight_updater, reward_engine):

        self.weight_updater = weight_updater
        self.reward_engine = reward_engine

    def step(self, pred, actual):

        reward = self.reward_engine.compute(pred, actual)

        self.weight_updater.update(pred, actual, reward)

        return {"reward": reward, "status": "updated"}
