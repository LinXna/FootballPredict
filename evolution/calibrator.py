import numpy as np


class Calibrator:
    """
    Temperature scaling calibration (stable heuristic version)
    """

    def __init__(self, temperature=1.15):
        self.temperature = temperature

    def calibrate(self, prob):

        if not isinstance(prob, dict):
            return {"H": 0.33, "D": 0.34, "A": 0.33}

        try:
            vec = np.array(
                [
                    float(prob.get("H", 0)),
                    float(prob.get("D", 0)),
                    float(prob.get("A", 0)),
                ]
            )
        except Exception:
            return {"H": 0.33, "D": 0.34, "A": 0.33}

        # temperature scaling
        vec = np.power(vec, 1 / self.temperature)

        vec = np.clip(vec, 1e-9, None)

        vec = vec / np.sum(vec)

        return {
            "H": float(vec[0]),
            "D": float(vec[1]),
            "A": float(vec[2]),
        }
