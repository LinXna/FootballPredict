class RewardEngine:
    """
    计算预测质量（reward signal）
    """

    def compute(self, pred, actual):
        """
        pred: {"H":, "D":, "A":}
        actual: 0/1/2
        """

        probs = [pred["H"], pred["D"], pred["A"]]

        # log loss style reward
        return -1.0 * (1 - probs[actual])
