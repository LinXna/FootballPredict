from models.elo_model import EloModel
from models.poisson_model import PoissonModel
from features.builder import FeatureBuilder
from ensemble.fusion import LearnedFusion
from data.odds_calibrator import odds_to_prob
from ensemble.market_fusion import MarketFusion

# =========================
# V1.8 Evolution Layer
# =========================
from evolution.drift_detector import DriftDetector
from evolution.calibrator import Calibrator


class Pipeline:
    def __init__(self):

        # =========================
        # Market Layer（不可删除）
        # =========================
        self.market_fusion = MarketFusion(alpha=0.7)

        # =========================
        # Base Models
        # =========================
        self.elo = EloModel()
        self.poisson = PoissonModel()

        # =========================
        # Features
        # =========================
        self.features = FeatureBuilder()

        # =========================
        # Fusion Layer
        # =========================
        self.fusion = LearnedFusion()

        # =========================
        # V1.8 Evolution Layer（新增）
        # =========================
        self.drift_detector = DriftDetector(window_size=50)
        self.calibrator = Calibrator()

    # =========================
    # Training
    # =========================
    def train(self, matches):

        for m in matches:
            self.elo.update(m["home"], m["away"], m["result"])
            self.features.train_update(m)

        self.poisson.train(matches)

    # =========================
    # 🎯 主预测入口（推荐）
    # =========================
    def predict(self, home, away, odds=None):

        # =========================
        # 1️⃣ Fusion base
        # =========================
        base = self.predict_fusion(home, away)

        # =========================
        # 2️⃣ Evolution Layer（V1.8新增）
        # =========================
        self.drift_detector.update(base)

        if self.drift_detector.detect():
            print("[V1.8 DRIFT] model distribution shift detected")

        base = self.calibrator.calibrate(base)

        # =========================
        # 3️⃣ Market Fusion（必须保留）
        # =========================
        if odds is not None:
            market_prob = odds_to_prob(odds)
            return self.market_fusion.fuse(base, market_prob)

        return base

    # =========================
    # 🔬 Elo raw
    # =========================
    def predict_raw(self, home, away):
        return self.elo.predict(home, away)

    # =========================
    # 🔬 Poisson raw
    # =========================
    def predict_poisson(self, home, away):
        return self.poisson.predict_1x2(home, away)

    # =========================
    # 🔬 Fusion core
    # =========================
    def predict_fusion(self, home, away):

        elo = self.elo.predict(home, away)
        poi = self.poisson.predict_1x2(home, away)

        return self.fusion.fuse(elo, poi)
