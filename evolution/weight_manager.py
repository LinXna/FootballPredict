class WeightManager:
    """
    控制 ensemble 权重动态变化
    """

    def __init__(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}

    def update(self, new_weights):
        self.weights = new_weights

    def get(self):
        return self.weights
