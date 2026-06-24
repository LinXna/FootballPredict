import numpy as np


class Calibrator:
    """
    概率校准（Platt Scaling 简化版）
    """

    def calibrate(self, prob):
        """
        prob: {"H":, "D":, "A":}
        """

        values = np.array(list(prob.values()))

        # soft calibration
        values = np.power(values, 1.2)

        values = values / np.sum(values)

        return {"H": float(values[0]), "D": float(values[1]), "A": float(values[2])}
