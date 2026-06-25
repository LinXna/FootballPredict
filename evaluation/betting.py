import logging

logger = logging.getLogger(__name__)


class BettingV2:

    def __init__(self, pipeline, threshold=0.08):
        self.pipeline = pipeline
        self.threshold = threshold
        self.bankroll = 100.0

    def run(self, matches):

        history = []

        for i, m in enumerate(matches):

            home = m.get("home")
            away = m.get("away")
            odds = m.get("odds")

            actual = m.get("result")

            if not home or not away or actual not in {"H", "D", "A"}:
                continue

            if not isinstance(odds, dict):
                continue

            try:
                pred = self.pipeline.predict(home, away, odds=odds)

                if not isinstance(pred, dict):
                    continue

                best = max(pred, key=pred.get)
                prob = pred[best]

                odd = odds.get(best)

                if odd is None:
                    continue

                odd = float(odd)

                ev = prob * odd - 1

                if ev < self.threshold:
                    continue

                stake = self.bankroll * 0.02

                if actual == best:
                    profit = stake * (odd - 1)
                else:
                    profit = -stake

                self.bankroll += profit

                history.append(
                    {
                        "match": i,
                        "bet": best,
                        "prob": prob,
                        "odds": odd,
                        "ev": ev,
                        "profit": profit,
                        "bankroll": self.bankroll,
                    }
                )

            except Exception as e:
                logger.warning(f"bet skip: {e}")
                continue

        return {"final_bankroll": self.bankroll, "history": history}
