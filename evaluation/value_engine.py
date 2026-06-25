class ValueEngineV2:

    def compute_ev(self, pred, odds):

        if not isinstance(pred, dict) or not isinstance(odds, dict):
            return {"H": 0, "D": 0, "A": 0}

        ev = {}

        for k in ["H", "D", "A"]:

            p = pred.get(k, 0.0)
            o = odds.get(k, 1.01)

            try:
                p = max(1e-9, min(float(p), 1 - 1e-9))
                o = max(1.01, float(o))
            except Exception:
                p, o = 0.0, 1.01

            ev[k] = p * o - 1

        return ev
