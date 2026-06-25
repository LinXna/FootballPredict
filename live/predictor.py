from live.adjuster import LiveAdjuster
from core.pipeline import Pipeline


class LivePredictor:

    def __init__(self, pipeline: Pipeline):

        self.pipeline = pipeline

        # adjuster now PURE weight scaler
        self.adjuster = LiveAdjuster()

    # =====================================================
    # MAIN PREDICT
    # =====================================================
    def predict(self, state):

        # -------------------------
        # 1. base prediction
        # -------------------------
        base = self._safe_base_predict(state)

        if not base:
            return self._default_prob()

        # -------------------------
        # 2. live adjustment (FIXED INTERFACE)
        # -------------------------
        adjusted = self._apply_adjustment(base)

        # -------------------------
        # 3. normalization
        # -------------------------
        return self._normalize(adjusted)

    # =====================================================
    # SAFE PIPELINE CALL
    # =====================================================
    def _safe_base_predict(self, state):

        try:
            return self.pipeline.predict(state.home, state.away)
        except Exception:
            return None

    # =====================================================
    # ADJUSTMENT (FIXED: no state leakage)
    # =====================================================
    def _apply_adjustment(self, base):

        try:
            # convert prob → pseudo delta weights
            delta = {
                "elo": (base.get("H", 0) - 0.33),
                "poisson": (base.get("A", 0) - 0.33),
            }

            adjusted = self.adjuster.adjust(delta)

            # merge adjustment softly (no overwrite)
            return {k: base.get(k, 0.33) * adjusted.get("elo", 0.5) for k in base}

        except Exception:
            return base

    # =====================================================
    # NORMALIZATION
    # =====================================================
    def _normalize(self, prob):

        try:
            total = sum(prob.values())

            if total <= 0:
                return self._default_prob()

            return {k: v / total for k, v in prob.items()}

        except Exception:
            return self._default_prob()

    # =====================================================
    # DEFAULT
    # =====================================================
    def _default_prob(self):
        return {"H": 0.33, "D": 0.34, "A": 0.33}

    # =====================================================
    # RAW DEBUG
    # =====================================================
    def predict_raw(self, state):

        try:
            return self.pipeline.predict(state.home, state.away)
        except Exception:
            return None
