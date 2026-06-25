import json
import os


class WeightUpdater:
    """
    V2.0 AI Adaptive Engine
    -----------------------
    Online Adaptive Weight Learning Engine

    Features:
    ✔ Online weight adaptation
    ✔ Match-level evaluation
    ✔ Persistent storage
    ✔ Stable normalization
    ✔ Fusion-compatible output
    """

    WEIGHT_FILE = "data/model_weights.json"

    def __init__(self):

        # =========================
        # Learning rate
        # =========================
        self.learning_rate = 0.02

        # =========================
        # Base weights
        # =========================
        self.weights = {"elo": 0.50, "poisson": 0.50}

        # =========================
        # Load persisted weights
        # =========================
        self._load()

    # =========================================================
    # Public API
    # =========================================================

    def current_weights(self):
        return dict(self.weights)

    def batch_update(self, samples):
        """
        samples:
        [
            {
                "prediction": {...},
                "result": "H|D|A",
                "context": {...}
            }
        ]
        """

        if not samples:
            return

        elo_total = 0.0
        poisson_total = 0.0

        for s in samples:

            elo_score, poisson_score = self._evaluate(s["prediction"], s["result"])

            elo_total += elo_score
            poisson_total += poisson_score

        n = len(samples)

        elo_avg = elo_total / n
        poisson_avg = poisson_total / n

        delta = elo_avg - poisson_avg

        # =========================
        # Adaptive update
        # =========================
        self.weights["elo"] += delta * self.learning_rate
        self.weights["poisson"] -= delta * self.learning_rate

        self._normalize()
        self._save()

    # =========================================================
    # Core evaluation
    # =========================================================

    def _evaluate(self, prediction, result):

        if not prediction:
            return 0.5, 0.5

        elo = prediction.get("elo", {})
        poi = prediction.get("poisson", {})

        elo_score = elo.get(result, 0.0)
        poisson_score = poi.get(result, 0.0)

        return elo_score, poisson_score

    # =========================================================
    # Normalization (critical stability layer)
    # =========================================================

    def _normalize(self):

        # prevent collapse
        for k in self.weights:
            self.weights[k] = max(0.05, self.weights[k])

        total = sum(self.weights.values())

        if total <= 0:
            self.weights = {"elo": 0.5, "poisson": 0.5}
            return

        for k in self.weights:
            self.weights[k] = round(self.weights[k] / total, 4)

    # =========================================================
    # Persistence layer
    # =========================================================

    def _save(self):

        os.makedirs(os.path.dirname(self.WEIGHT_FILE), exist_ok=True)

        with open(self.WEIGHT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.weights, f, indent=4)

    def _load(self):

        if not os.path.exists(self.WEIGHT_FILE):
            return

        try:
            with open(self.WEIGHT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                if "elo" in data and "poisson" in data:
                    self.weights = {
                        "elo": float(data["elo"]),
                        "poisson": float(data["poisson"]),
                    }

        except Exception:
            self.weights = {"elo": 0.5, "poisson": 0.5}

    # =========================================================
    # Debug tools
    # =========================================================

    def reset(self):
        self.weights = {"elo": 0.5, "poisson": 0.5}
        self._save()

    def __repr__(self):
        return f"WeightUpdater(elo={self.weights['elo']}, poisson={self.weights['poisson']})"
