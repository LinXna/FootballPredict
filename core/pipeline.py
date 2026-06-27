from models.elo_model import EloModel
from models.poisson_model import PoissonModel
from ensemble.fusion import FusionEngine
from data.odds_calibrator import odds_to_prob


class Pipeline:
    def __init__(self):
        self.elo = EloModel()
        self.poisson = PoissonModel()
        self.fusion = FusionEngine()

    def initialize(self):
        pass

    def predict(self, home, away, odds=None):
        elo_p = self.elo.predict(home, away)
        poi_p = self.poisson.predict_1x2(home, away)

        model_p = self.fusion.fuse(elo_p, poi_p)

        if odds:
            market_p = odds_to_prob(odds)
            model_p = self.fusion.market_fuse(model_p, market_p)

        return self._normalize(model_p)

    def _normalize(self, p):
        s = sum(p.values())
        return {k: v / s for k, v in p.items()}

    def train(self, matches):
        """
        V3.5 收敛训练入口
        """

        for m in matches:
            home = m["home"]
            away = m["away"]
            result = m["result"]

            # Elo update
            self.elo.update(home, away, result)

            # Poisson update
            self.poisson.train([m])

        return True
