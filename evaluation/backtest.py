import logging
from evaluation.metrics import logloss, brier_score

logger = logging.getLogger(__name__)


class BacktestV2:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, matches):

        total_logloss = 0.0
        total_brier = 0.0

        correct = 0
        valid = 0
        rejected = 0

        reject_log = []

        for i, m in enumerate(matches):

            # -----------------------
            # strict validation
            # -----------------------
            home = m.get("home")
            away = m.get("away")
            result = m.get("result")

            if not home or not away or result not in {"H", "D", "A"}:
                rejected += 1
                reject_log.append((i, "invalid_match"))
                continue

            try:
                pred = self.pipeline.predict(home, away, odds=m.get("odds"))

                if not isinstance(pred, dict):
                    raise ValueError("invalid_pred")

                if not all(k in pred for k in ["H", "D", "A"]):
                    raise ValueError("missing_keys")

                actual = result

                total_logloss += logloss(pred, actual)
                total_brier += brier_score(pred, actual)

                if max(pred, key=pred.get) == actual:
                    correct += 1

                valid += 1

            except Exception as e:
                rejected += 1
                reject_log.append((i, str(e)))

        if valid == 0:
            return {
                "accuracy": 0,
                "logloss": 0,
                "brier": 0,
                "valid": 0,
                "rejected": rejected,
            }, reject_log

        return {
            "accuracy": correct / valid,
            "logloss": total_logloss / valid,
            "brier": total_brier / valid,
            "valid": valid,
            "rejected": rejected,
        }, reject_log
