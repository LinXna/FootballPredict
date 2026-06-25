import logging
from evaluation.metrics import logloss, brier_score

logger = logging.getLogger(__name__)


class BenchmarkV2:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, matches):

        results = {
            "elo": {"logloss": 0, "brier": 0, "count": 0},
            "poisson": {"logloss": 0, "brier": 0, "count": 0},
            "fusion": {"logloss": 0, "brier": 0, "count": 0},
        }

        rejected = 0

        for i, m in enumerate(matches):

            home = m.get("home")
            away = m.get("away")
            actual = m.get("result")

            if not home or not away or actual not in {"H", "D", "A"}:
                rejected += 1
                continue

            models = {
                "elo": self.pipeline.predict_raw,
                "poisson": self.pipeline.predict_poisson,
                "fusion": self.pipeline.predict_fusion,
            }

            for name, fn in models.items():

                try:
                    pred = fn(home, away)

                    if not isinstance(pred, dict):
                        raise ValueError("bad_pred")

                    if not all(k in pred for k in ["H", "D", "A"]):
                        raise ValueError("missing_keys")

                    results[name]["logloss"] += logloss(pred, actual)
                    results[name]["brier"] += brier_score(pred, actual)
                    results[name]["count"] += 1

                except Exception:
                    rejected += 1
                    continue

        for name in results:
            c = results[name]["count"]
            if c > 0:
                results[name]["logloss"] /= c
                results[name]["brier"] /= c

        results["rejected"] = rejected
        return results
