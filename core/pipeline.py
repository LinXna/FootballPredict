# core/pipeline.py

import logging

from models.elo_model import EloModel
from models.poisson_model import PoissonModel
from features.builder import FeatureBuilder
from ensemble.fusion import LearnedFusion
from data.odds_calibrator import odds_to_prob
from ensemble.market_fusion import MarketFusion
from evolution.drift_detector import DriftDetector
from evolution.calibrator import Calibrator

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self):

        self.market_fusion = MarketFusion(alpha=0.7)

        self.elo = EloModel()
        self.poisson = PoissonModel()

        self.features = FeatureBuilder()

        self.fusion = LearnedFusion()

        self.drift_detector = DriftDetector(window_size=50)
        self.calibrator = Calibrator()

    # =========================
    # Training
    # =========================
    def train(self, matches):

        for m in matches:

            try:
                home = m.get("home")
                away = m.get("away")
                result = m.get("result")

                if not home or not away or result not in ["H", "D", "A"]:
                    continue

                self.elo.update(home, away, result)
                self.features.train_update(m)

            except Exception as e:
                logger.warning(f"train skip match: {e}")

        self.poisson.train(matches)

    # =========================
    # Predict
    # =========================
    def predict(self, home, away, odds=None):

        if not home or not away:
            raise ValueError("invalid input")

        base = self.predict_fusion(home, away)

        # drift protection
        try:
            self.drift_detector.update(base)
            if self.drift_detector.detect():
                logger.warning("drift detected")
        except Exception:
            pass

        try:
            base = self.calibrator.calibrate(base)
        except Exception:
            pass

        # market fusion
        if odds is not None:
            try:
                market_prob = odds_to_prob(odds)
                return self.market_fusion.fuse(base, market_prob)
            except Exception:
                return base

        return base

    # =========================
    # Raw models
    # =========================
    def predict_raw(self, home, away):
        return self.elo.predict(home, away)

    def predict_poisson(self, home, away):
        return self.poisson.predict_1x2(home, away)

    def predict_fusion(self, home, away):
        elo = self.elo.predict(home, away)
        poi = self.poisson.predict_1x2(home, away)
        return self.fusion.fuse(elo, poi)
