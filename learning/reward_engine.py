class RewardEngine:
    """
    V2.1 Reward System
    ------------------
    Convert prediction error into learning signal
    """

    def compute(self, prediction, actual):

        pred_label = max(
            prediction["probabilities"], key=prediction["probabilities"].get
        )

        reward = 1.0 if pred_label == actual else -1.0

        confidence = prediction.get("confidence", 0.5)

        # confidence-weighted reward
        return reward * confidence
