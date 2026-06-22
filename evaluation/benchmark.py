from evaluation.metrics import logloss, brier_score


class ModelBenchmark:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, matches):

        models = {
            "elo": lambda m: self.pipeline.predict_raw(m["home"], m["away"]),
            "poisson": lambda m: self.pipeline.predict_poisson(m["home"], m["away"]),
            "fusion": lambda m: self.pipeline.predict_fusion(m["home"], m["away"]),
            # =========================
            # V1-FREEZE: market is pipeline mode
            # =========================
            "market": lambda m: self.pipeline.predict(
                m["home"], m["away"], odds=m["odds"]
            ),
        }

        results = {name: {"logloss": 0, "brier": 0, "count": 0} for name in models}

        for m in matches:

            actual = str(m["result"]).strip().upper()

            for name, fn in models.items():

                pred = fn(m)

                results[name]["logloss"] += logloss(pred, actual)
                results[name]["brier"] += brier_score(pred, actual)
                results[name]["count"] += 1

        for name in results:

            c = results[name]["count"]

            if c == 0:
                continue

            results[name]["logloss"] /= c
            results[name]["brier"] /= c

        return results
